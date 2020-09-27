# Copyright (C) 2019 Konos
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class BcCertification(models.Model):
    _name = "bc.certification"
    _description = "Certification"

    name = fields.Char("Name")
    bc_issuer_id = fields.Many2one("bc.issuer", "Issuer",)
    partner_id = fields.Many2one("res.partner", "Partner",)
    company_id = fields.Many2one("res.company", "Company",)
    bc_certification_template = fields.Many2one(
        "bc.certification.template", "Template",
    )
