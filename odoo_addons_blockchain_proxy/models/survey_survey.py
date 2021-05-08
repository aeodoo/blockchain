from odoo import api, fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    is_blockchain_certification = fields.Boolean("Blockchain Certification")

    @api.onchange("is_blockchain_certification")
    def on_change_is_blockchain_certification(self):
        for record in self:
            if record.is_blockchain_certification:
                record.is_time_limited = True
                record.questions_selection = "all"
                record.users_can_go_back = True
                record.scoring_type = "scoring_with_answers"
                record.passing_score = 90
                record.certificate = True
                if not record.certification_mail_template_id:
                    record.certification_mail_template_id = record.env.ref(
                        "survey.mail_template_certification"
                    )
                record.certification_give_badge = True
                record.access_mode = "token"
                record.users_login_required = True
                record.is_attempts_limited = True
