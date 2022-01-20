# -*- coding: utf-8 -*-

from odoo import models, fields, api


class barcode_configuration(models.Model):
    _name = 'barcode.print.configuration'
    _description = 'barcode print configuration'

    item_name_x1 = fields.Integer()
    item_name_y1 = fields.Integer()

    item_variant_x1 = fields.Integer()
    item_variant_y1 = fields.Integer()

    dimensions_x1 = fields.Integer()
    dimensions_y1 = fields.Integer()

    size_x1 = fields.Integer()
    size_y1 = fields.Integer()

    date_x1 = fields.Integer()
    date_y1 = fields.Integer()

    quantity_x1 = fields.Integer()
    quantity_y1 = fields.Integer()

    price_state1_x = fields.Integer()

    price_state1_y1 = fields.Integer()
    price_state2_y1 = fields.Integer()
    price_state3_y1 = fields.Integer()
    price_state4_y1 = fields.Integer()
    price_state5_y1 = fields.Integer()
    price_state6_y1 = fields.Integer()
    price_state7_y1 = fields.Integer()
    price_state8_y1 = fields.Integer()
    price_state9_y1 = fields.Integer()
    price_state10_y1 = fields.Integer()
    price_state11_y1 = fields.Integer()

    barcode_x1 = fields.Integer()
    barcode_y1 = fields.Integer()




