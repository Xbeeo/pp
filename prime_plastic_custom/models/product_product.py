# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    product_color_id = fields.Many2one("color.color", string="Product Color" ,related='product_tmpl_id.product_color_id', store=True)
    product_model_id = fields.Many2one("product.model", string="Product Model" , related='product_tmpl_id.product_model_id', store=True)
    product_material_id = fields.Many2one("material.material", string="Product Material", related='product_tmpl_id.product_material_id', store=True)
    product_standard_weight = fields.Float(string="Product Standard Weight (kg)")