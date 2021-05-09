from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _get_mandatory_billing_fields(self):
        res = super()._get_mandatory_billing_fields()
        order = request.website.sale_get_order()
        if order and order.is_blockchain_certification:
            res.append("public_address")
        return res

    def _get_mandatory_shipping_fields(self):
        res = super()._get_mandatory_shipping_fields()
        order = request.website.sale_get_order()
        if order and order.is_blockchain_certification:
            res.append("public_address")
        return res

    def _checkout_form_save(self, mode, checkout, all_values):
        partner_id = super()._checkout_form_save(mode, checkout, all_values)
        partner_id = request.env["res.partner"].browse(partner_id)
        partner_id.sudo().write({"public_address": all_values["public_address"]})
        return partner_id.id
