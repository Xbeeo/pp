# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'
    _description = 'Stock Picking'
    transport_driver_id = fields.Many2one(
        comodel_name='sale.driver',
        string='Driver Name',
        compute='_compute_transport_info',
        store=True,
        readonly=True,
    )
    transport_vehicle_id = fields.Many2one(
        comodel_name='transport.vehicle',
        string='Vehicle No.',
        compute='_compute_transport_info',
        store=True,
        readonly=True,
    )

    @api.depends(
        "sale_id",
        "sale_id.transport_driver_id",
        "sale_id.transport_vehicle_id",
        "purchase_id",
        "purchase_id.transport_driver_id",
        "purchase_id.transport_vehicle_id",
    )
    def _compute_transport_info(self):
        for picking in self:

            if picking.sale_id:
                picking.transport_driver_id = picking.sale_id.transport_driver_id
                picking.transport_vehicle_id = picking.sale_id.transport_vehicle_id

            elif picking.purchase_id:
                picking.transport_driver_id = picking.purchase_id.transport_driver_id
                picking.transport_vehicle_id = picking.purchase_id.transport_vehicle_id

            else:
                picking.transport_driver_id = False
                picking.transport_vehicle_id = False

    @api.model_create_multi
    def create(self, vals_list):
        confirm_user = self.env.context.get('confirm_user_id')

        if confirm_user:
            for vals in vals_list:
                vals['user_id'] = confirm_user

        return super().create(vals_list)