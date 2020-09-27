# Copyright (c) 2019 Open Source Integrators
# Copyright (C) 2019 Konos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class BcIssuerKey(models.Model):
    _name = "bc.issuer.key"
    _description = "Issuer"

    date = fields.Date("Date")
    bc_issuer_id = fields.Many2one(
        "bc.issuer", "Issuer", required=True,
    )
