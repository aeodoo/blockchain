# Copyright (c) 2019 Open Source Integrators
# Copyright (C) 2019 Konos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class BcIssuer(models.Model):
    _name = "bc.issuer"
    _description = "Issuer"

    name = fields.Char("Name")
    company_id = fields.Many2one(
        "res.company", "Company", required=True, default=lambda self: self.env.company,
    )
    bc_issuer_key_ids = fields.One2many(
        "bc.issuer.key", "bc_issuer_id", help="Issuer Keys",
    )
    logo_file = fields.Binary(string="Issuer Logo", store=True, attachment=True)
    issuer_url = fields.Char("Issuer URL", size=1024)
    email = fields.Char(string="Email")
