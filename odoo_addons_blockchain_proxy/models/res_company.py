from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    data_dir = fields.Char("Data directory", default="/data_dir")
    template_dir = fields.Char("Template directory", default="/template_dir")
    template_name = fields.Char("Template name", default="/template_name")
    template_content = fields.Html("Template content")

    issuer_id = fields.Char("Issuer ID")
    issuer_key = fields.Char("Issuer private key")
    issuer_public_key = fields.Char("Issuer public key")
