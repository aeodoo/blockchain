from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventEvent(models.Model):
    _inherit = "event.event"

    is_blockchain_certification = fields.Boolean("Blockchain Certification")
    survey_id = fields.Many2one(comodel_name="survey.survey")

    @api.onchange("is_blockchain_certification")
    def on_change_is_blockchain_certification(self):
        for record in self:
            if record.is_blockchain_certification:
                record.is_online = True
                record.auto_confirm = True
                record.seats_avaliability = "limited"

    def button_confirm(self):
        for event_id in self:
            if not event_id.survey_id:
                raise ValidationError(_("You must fill a certification survey"))
        return super().button_confirm()
