# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    transport_driver_id = fields.Many2one(
        comodel_name='sale.driver',
        string='Driver Name',
        required=True,
    )
    transport_vehicle_id = fields.Many2one(
        comodel_name='transport.vehicle',
        string='Vehicle No.',
        required=True,
    )

    def action_confirm(self):
        res = super(
            SaleOrder,
            self.with_context(confirm_user_id=self.env.user.id)
        ).action_confirm()
        for order in self:
            for picking in order.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel')):
                picking.action_assign()
                for move in picking.move_ids:
                    move.quantity = move.product_uom_qty
                picking.button_validate()
            if order.invoice_status == 'to invoice':
                invoices = order._create_invoices()
                invoices.action_post()
        return res