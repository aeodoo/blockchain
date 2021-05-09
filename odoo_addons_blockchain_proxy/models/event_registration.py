from odoo import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def confirm_registration(self):
        res = super().confirm_registration()
        if self.sale_order_id.is_blockchain_certification:
            partner_ids = [(6, 0, [self.sale_order_id.partner_id.id])]
            event_id = self.sale_order_line_id.event_id
            template_id = self.env.ref("survey.mail_template_user_input_invite")
            invite_id = self.env["survey.invite"].create(
                {
                    "survey_id": event_id.survey_id.id,
                    "partner_ids": partner_ids,
                    "deadline": event_id.date_end,
                    "emails": self.sale_order_id.partner_id.email,
                    "subject": template_id.subject,
                    "body": template_id.body_html,
                }
            )
            invite_id.action_invite()
        user_ids = self.env["res.users"].search(
            [("partner_id", "=", self.sale_order_id.partner_id.id)]
        )
        if not user_ids:
            portal_wizard_id = self.env["portal.wizard"].create(
                {
                    "user_ids": [
                        (
                            0,
                            0,
                            {
                                "partner_id": self.sale_order_id.partner_id.id,
                                "email": self.sale_order_id.partner_id.email,
                                "in_portal": True,
                            },
                        )
                    ]
                }
            )
            portal_wizard_id.action_apply()
        return res
