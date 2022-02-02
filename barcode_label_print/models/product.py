# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,_,api

class ProductBrand(models.Model):
    _inherit = 'product.product'

    dimensions = fields.Char(string='Dimensions')
    content = fields.Char(string='Content')
    suffix = fields.Char(string='Suffix',default="AB")
    serial_no = fields.Integer(string='Serial NO')