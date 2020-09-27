# Copyright (c) 2019 Open Source Integrators
# Copyright (C) 2019 Konos
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class BcCertificationTemplate(models.Model):
    _name = "bc.certification.template"
    _description = "Certification Template"

    name = fields.Char("Name")
    issuer_id = fields.Many2one("bc.issuer", "Issuer",)
    company_id = fields.Many2one("res.company", "Company",)
    cert_image_file = fields.Binary(
        string="Certification Logo", store=True, attachment=True
    )
    certificate_description = fields.Text("Description", translate=True)
    certificate_title = fields.Text("Tittle", translate=True)
    criteria_narrative = fields.Text("Criteria Narrative", translate=True)
