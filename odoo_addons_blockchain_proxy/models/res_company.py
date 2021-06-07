from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    environment = fields.Selection(
        [("ethereum_ropsten", "Test"), ("ethereum_mainnet", "Production")],
        "Environment",
        default="ethereum_ropsten",
    )
    cert_issuer_path = fields.Char("Cert-issuer path")
    email = fields.Char(required=True)
    data_dir = fields.Char("Data directory", default="/data_dir")

    issuer_id = fields.Char("Issuer ID")
    issuer_key = fields.Char("Issuer private key")
    issuer_public_key = fields.Char("Issuer public key")
    issuer_certs_url = fields.Char("Issuer URL")

    gas_limit = fields.Integer("Gas limit", default=20000)
    etherscan_api_token = fields.Char("Etherscan Token")
