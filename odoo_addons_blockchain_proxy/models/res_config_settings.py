from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_odoo_addons_blockchain_proxy = fields.Boolean("Blockchain module")
