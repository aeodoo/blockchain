from odoo import fields, models


class GamificationBadge(models.Model):
    _inherit = "gamification.badge"

    criteria_narrative = fields.Html("Criteria Narrative", translate=True)
