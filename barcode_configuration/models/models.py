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

    def search_function(self,product_id):

        attribute_id = self.env['product.attribute'].sudo().search([('name', 'like', '%SIZE%')]).id
        print('attribute_id',attribute_id)
        if attribute_id:
            query = self._cr.execute("""
                                     select pdt_temp.id,pdt_temp.name,pdt_temp.content,pdt_temp.dimensions,pdt_pdt.barcode,
                    pdt_temp.list_price,pdt_att.name AS attribute_name,pdt_att_val.name AS attribute_value  from product_template As pdt_temp 
                    left join product_product AS pdt_pdt on pdt_temp.id=pdt_pdt.product_tmpl_id
                    left join product_template_attribute_line AS pdt_att_line on pdt_temp.id=pdt_att_line.product_tmpl_id
                    left join product_attribute AS pdt_att on pdt_att.id=pdt_att_line.attribute_id
                    left join product_attribute_value AS pdt_att_val on pdt_att.id=pdt_att_val.attribute_id
                    WHERE pdt_att.id = %s and pdt_temp.id in %s """, (attribute_id, tuple([product_id]),))
            res = self._cr.dictfetchall()
            print('result',res)
            # res_dumps = json.dumps(res)
            # print('res_dumps', res_dumps)
            return res




