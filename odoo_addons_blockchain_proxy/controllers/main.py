import logging

from werkzeug.exceptions import Forbidden

from odoo import _, http, tools
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.website.controllers.main import Website

_logger = logging.getLogger(__name__)


class Website(Website):
    def checkout_redirection(self, order):
        # must have a draft sales order with lines at this point, otherwise reset
        if not order or order.state != "draft":
            request.session["sale_order_id"] = None
            request.session["sale_transaction_id"] = None
            return request.redirect("/shop")

        if order and not order.order_line:
            return request.redirect("/shop/cart")

        # if transaction pending / done: redirect to confirmation
        tx = request.env.context.get("website_sale_transaction")
        if tx and tx.state != "draft":
            return request.redirect("/shop/payment/confirmation/%s" % order.id)

    def checkout_form_validate(self, mode, all_form_values, data):
        # mode: tuple ('new|edit', 'billing|shipping')
        # all_form_values: all values before preprocess
        # data: values after preprocess
        error = dict()
        error_message = []

        # Required fields from form
        required_fields = [
            f for f in (all_form_values.get("field_required") or "").split(",") if f
        ]
        # Required fields from mandatory field function
        required_fields += (
            mode[1] == "shipping"
            and self._get_mandatory_shipping_fields()
            or self._get_mandatory_billing_fields()
        )
        # Check if state required
        country = request.env["res.country"]
        if data.get("country_id"):
            country = country.browse(int(data.get("country_id")))
            if "state_code" in country.get_address_fields() and country.state_ids:
                required_fields += ["state_id"]

        # error message for empty required fields
        for field_name in required_fields:
            if not data.get(field_name):
                error[field_name] = "missing"

        # email validation
        if data.get("email") and not tools.single_email_re.match(data.get("email")):
            error["email"] = "error"
            error_message.append(
                _("Invalid Email! Please enter a valid email address.")
            )

        # vat validation
        Partner = request.env["res.partner"]
        if data.get("vat") and hasattr(Partner, "check_vat"):
            if data.get("country_id"):
                data["vat"] = Partner.fix_eu_vat_number(
                    data.get("country_id"), data.get("vat")
                )
            partner_dummy = Partner.new(
                {
                    "vat": data["vat"],
                    "country_id": (
                        int(data["country_id"]) if data.get("country_id") else False
                    ),
                }
            )
            try:
                partner_dummy.check_vat()
            except ValidationError:
                error["vat"] = "error"

        if [err for err in error.values() if err == "missing"]:
            error_message.append(_("Some required fields are empty."))

        return error, error_message

    def _get_mandatory_billing_fields(self):
        return ["name", "email", "street", "city", "country_id", "public_address"]

    def values_preprocess(self, order, mode, values):
        # Convert the values for many2one fields to integer since they are used as IDs
        partner_fields = request.env["res.partner"]._fields
        return {
            k: (bool(v) and int(v))
            if k in partner_fields and partner_fields[k].type == "many2one"
            else v
            for k, v in values.items()
        }

    def values_postprocess(self, order, mode, values, errors, error_msg):
        new_values = {}
        authorized_fields = (
            request.env["ir.model"]._get("res.partner")._get_form_writable_fields()
        )
        for k, v in values.items():
            # don't drop empty value, it could be a field to reset
            if k in authorized_fields and v is not None:
                new_values[k] = v
            else:  # DEBUG ONLY
                if k not in (
                    "field_required",
                    "partner_id",
                    "callback",
                    "submitted",
                ):  # classic case
                    _logger.debug(
                        "website_sale postprocess: %s value "
                        "has been dropped (empty or not writable)" % k
                    )

        new_values["team_id"] = (
            request.website.salesteam_id and request.website.salesteam_id.id
        )
        new_values["user_id"] = (
            request.website.salesperson_id and request.website.salesperson_id.id
        )

        if request.website.specific_user_account:
            new_values["website_id"] = request.website.id

        if mode[0] == "new":
            new_values["company_id"] = request.website.company_id.id

        lang = (
            request.lang.code
            if request.lang.code in request.website.mapped("language_ids.code")
            else None
        )
        if lang:
            new_values["lang"] = lang
        if mode == ("edit", "billing") and order.partner_id.type == "contact":
            new_values["type"] = "other"
        if mode[1] == "shipping":
            new_values["parent_id"] = order.partner_id.commercial_partner_id.id
            new_values["type"] = "delivery"

        return new_values, errors, error_msg

    @http.route(
        ["/shop/address"],
        type="http",
        methods=["GET", "POST"],
        auth="public",
        website=True,
        sitemap=False,
    )
    def address(self, **kw):
        Partner = request.env["res.partner"].with_context(show_address=1).sudo()
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        mode = (False, False)
        can_edit_vat = False
        def_country_id = order.partner_id.country_id
        values, errors = {}, {}

        partner_id = int(kw.get("partner_id", -1))

        # IF PUBLIC ORDER
        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            mode = ("new", "billing")
            can_edit_vat = True
            country_code = request.session["geoip"].get("country_code")
            if country_code:
                def_country_id = request.env["res.country"].search(
                    [("code", "=", country_code)], limit=1
                )
            else:
                def_country_id = request.website.user_id.sudo().country_id
        # IF ORDER LINKED TO A PARTNER
        else:
            if partner_id > 0:
                if partner_id == order.partner_id.id:
                    mode = ("edit", "billing")
                    can_edit_vat = order.partner_id.can_edit_vat()
                else:
                    shippings = Partner.search(
                        [("id", "child_of", order.partner_id.commercial_partner_id.ids)]
                    )
                    if partner_id in shippings.mapped("id"):
                        mode = ("edit", "shipping")
                    else:
                        return Forbidden()
                if mode:
                    values = Partner.browse(partner_id)
            elif partner_id == -1:
                mode = ("new", "shipping")
            else:  # no mode - refresh without post?
                return request.redirect("/shop/checkout")

        # IF POSTED
        if "submitted" in kw:
            pre_values = self.values_preprocess(order, mode, kw)
            errors, error_msg = self.checkout_form_validate(mode, kw, pre_values)
            post, errors, error_msg = self.values_postprocess(
                order, mode, pre_values, errors, error_msg
            )

            if errors:
                errors["error_message"] = error_msg
                values = kw
            else:
                partner_id = self._checkout_form_save(mode, post, kw)
                if mode[1] == "billing":
                    order.partner_id = partner_id
                    order.with_context(not_self_saleperson=True).onchange_partner_id()
                    # This is the *only* thing that the front end
                    # user will see/edit anyway when choosing billing address
                    order.partner_invoice_id = partner_id
                    if not kw.get("use_same"):
                        kw["callback"] = kw.get("callback") or (
                            not order.only_services
                            and (
                                mode[0] == "edit"
                                and "/shop/checkout"
                                or "/shop/address"
                            )
                        )
                elif mode[1] == "shipping":
                    order.partner_shipping_id = partner_id

                order.message_partner_ids = [
                    (4, partner_id),
                    (3, request.website.partner_id.id),
                ]
                if not errors:
                    return request.redirect(kw.get("callback") or "/shop/confirm_order")

        country = (
            "country_id" in values
            and values["country_id"] != ""
            and request.env["res.country"].browse(int(values["country_id"]))
        )
        country = country and country.exists() or def_country_id
        render_values = {
            "website_sale_order": order,
            "partner_id": partner_id,
            "mode": mode,
            "checkout": values,
            "can_edit_vat": can_edit_vat,
            "country": country,
            "countries": country.get_website_sale_countries(mode=mode[1]),
            "states": country.get_website_sale_states(mode=mode[1]),
            "error": errors,
            "callback": kw.get("callback"),
            "only_services": order and order.only_services,
        }
        return request.render(
            "odoo_addons_blockchain_proxy.address_with_blockchain", render_values
        )
