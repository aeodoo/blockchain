from odoo import api, models


class Users(models.Model):
    _inherit = "res.users"

    @api.model
    def _get_partner_public_address(self, vals):
        if "partner_id" in vals:
            public_address = (
                self.env["res.partner"].browse(vals["partner_id"]).public_address
            )
            vals["public_address"] = public_address
        return vals

    @api.model
    def create(self, vals):
        return super().create(self._get_partner_public_address(vals))

    def write(self, vals):
        return super().write(self._get_partner_public_address(vals))
