
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit ='product.template'

    dimensions = fields.Char(string='Dimensions (in mm)')
    content = fields.Char(string='Content')