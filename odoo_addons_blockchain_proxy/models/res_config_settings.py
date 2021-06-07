from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_odoo_addons_blockchain_proxy = fields.Boolean("Blockchain module")

    environment = fields.Selection(related="company_id.environment", readonly=False)
    cert_issuer_path = fields.Char(
        "Cert-issuer path", related="company_id.cert_issuer_path", readonly=False
    )
    data_dir = fields.Char(
        "Data directory", related="company_id.data_dir", readonly=False
    )
    issuer_id = fields.Char("Issuer ID", related="company_id.issuer_id", readonly=False)
    issuer_key = fields.Char(
        "Issuer private key", related="company_id.issuer_key", readonly=False
    )
    issuer_public_key = fields.Char(
        "Issuer public key", related="company_id.issuer_public_key", readonly=False
    )
    issuer_certs_url = fields.Char(
        "Issuer URL", related="company_id.issuer_certs_url", readonly=False
    )
    gas_limit = fields.Integer(
        "Gas limit", related="company_id.gas_limit", readonly=False
    )
    etherscan_api_token = fields.Char(
        "Etherscan Token", related="company_id.etherscan_api_token", readonly=False
    )
