from odoo import api, fields, models


class BcCertificationTemplate(models.Model):
    _inherit = "bc.certification.template"

    badge_id = fields.Many2one(comodel_name="gamification.badge", string="Badge")

    @api.onchange("badge_id")
    def on_change_badge_id(self):
        for record in self:
            if record.badge_id:
                record.cert_image_file = record.badge_id.image_1920
                record.certificate_description = record.badge_id.description
