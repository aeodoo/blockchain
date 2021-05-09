from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    public_address = fields.Char(string="Public Address", index=True)

    _sql_constraints = [
        (
            "public_address",
            "unique(public_address, active)",
            "This public address already exist",
        )
    ]

    @api.onchange("public_address")
    def _on_change_public_address(self):
        self.public_address = str(self.public_address).lower()
