from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_standard_weight = fields.Float(
        string="P.S.W (kg)",
        related='product_id.product_standard_weight',
        readonly=True,
        digits='Stock Weight',
    )
    receiving_weight = fields.Float(
        string="Rec.Weight (kg)",
        compute='_compute_receiving_weight',
        digits='Stock Weight',
    )

    @api.depends('move_ids.receiving_weight', 'move_ids.state')
    def _compute_receiving_weight(self):
        for line in self:
            moves = line.move_ids.filtered(lambda m: m.state != 'cancel')
            line.receiving_weight = sum(moves.mapped('receiving_weight'))