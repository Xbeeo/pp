from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_standard_weight = fields.Float(
        string="P.S.W (kg)",
        related='product_id.product_standard_weight',
        readonly=True,
        digits='Stock Weight',
    )
    receiving_weight = fields.Float(
        string="Rec.Weight (kg)",
        digits='Stock Weight',
    )