from odoo import models, fields


class VehicleNo(models.Model):
    _name = 'transport.vehicle'
    _description = 'Vehicle Number'
    _rec_name = 'vehicle_no'
    _order = 'vehicle_no asc'

    vehicle_no = fields.Char(
        string='Vehicle No.',
        required=True,
    )

    _sql_constraints = [
        ('vehicle_no_unique', 'UNIQUE(vehicle_no)', 'Vehicle number must be unique!'),
    ]