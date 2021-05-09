from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_blockchain_certification = fields.Boolean(
        string="Blockchain Certification",
        compute="_compute_is_blockchain_certification",
    )

    def _compute_is_blockchain_certification(self):
        for order_id in self:
            order_id.is_blockchain_certification = len(
                order_id.order_line.filtered(
                    lambda l: l.event_id.is_blockchain_certification
                    if l.event_id
                    else False
                )
            )
