from odoo import models, fields

class SaleDriver(models.Model):
    _name = 'sale.driver'
    _description = 'Driver'

    name = fields.Char(string='Driver Name', required=True)