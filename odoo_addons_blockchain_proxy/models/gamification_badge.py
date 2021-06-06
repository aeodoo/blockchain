from odoo import fields, models


class GamificationBadge(models.Model):
    _inherit = "gamification.badge"

    criteria_narrative = fields.Html("Criteria Narrative", translate=True)
    template_content = fields.Html("Template content")

    def action_create_template(self):
        for badge_id in self:
            badge_id.template_content = self.env.company.name
