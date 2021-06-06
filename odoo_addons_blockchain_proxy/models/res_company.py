from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    email = fields.Char(required=True)
    data_dir = fields.Char("Data directory", default="/data_dir")
    template_dir = fields.Char("Template directory", default="/template_dir")

    issuer_id = fields.Char("Issuer ID")
    issuer_key = fields.Char("Issuer private key")
    issuer_public_key = fields.Char("Issuer public key")
