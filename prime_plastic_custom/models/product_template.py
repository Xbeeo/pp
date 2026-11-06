# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    product_color_id = fields.Many2one("color.color", string="Product Color")
    product_model_id = fields.Many2one("product.model", string="Product Model")
    product_material_id = fields.Many2one("material.material", string="Product Material")
    product_standard_weight = fields.Float(string="Product Standard Weight (kg)")