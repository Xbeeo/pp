# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    transport_driver_id = fields.Many2one(
        "sale.driver",
        string="Driver Name",
        required=True,
    )

    transport_vehicle_id = fields.Many2one(
        "transport.vehicle",
        string="Vehicle No.",
        required=True,
    )

    def button_confirm(self):
        res = super(
            PurchaseOrder,
            self.with_context(confirm_user_id=self.env.user.id)
        ).button_confirm()

        for order in self:

            # Validate Receipts
            for picking in order.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
                picking.action_assign()

                for move in picking.move_ids:
                    move.quantity = move.product_uom_qty

                picking.button_validate()

            # Create Vendor Bill
            bills = order.action_create_invoice()

            if bills:
                if isinstance(bills, dict):
                    bill = self.env["account.move"].browse(bills.get("res_id"))
                else:
                    bill = bills

                if bill:
                    # Set Bill Date to today
                    bill.invoice_date = fields.Date.context_today(self)

                    # Post the bill
                    bill.action_post()

        return res