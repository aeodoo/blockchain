from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_odoo_addons_blockchain_proxy = fields.Boolean("Blockchain module")

    data_dir = fields.Char(
        "Data directory", related="company_id.data_dir", readonly=False
    )
    template_dir = fields.Char(
        "Template directory", related="company_id.template_dir", readonly=False
    )
    template_name = fields.Char(
        "Template name", related="company_id.template_name", readonly=False
    )
    template_content = fields.Html(
        "Template content", related="company_id.template_content", readonly=False
    )
    issuer_id = fields.Char("Issuer ID", related="company_id.issuer_id", readonly=False)
    issuer_key = fields.Char(
        "Issuer private key", related="company_id.issuer_key", readonly=False
    )
    issuer_public_key = fields.Char(
        "Issuer public key", related="company_id.issuer_public_key", readonly=False
    )

    def action_create_template(self):
        self.env.company.template_content = self.env.company.name
