from odoo import fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    blockchain_published = fields.Boolean("Published on blockchain", default=False)
