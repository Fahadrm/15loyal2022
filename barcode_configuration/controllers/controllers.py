# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import Response, request
import json



class BarcodeConfiguration(http.Controller):
    @http.route('/barcode_configuration/<int:product_id>', auth='public',type='json',methods=['POST','GET'])
    # @http.route('/barcode_configuration', auth='public',type="json",methods=['POST','GET'])
    def index(self, **kw):
        print('kwww',kw)
        product_id = kw.get('product_id')
        attribute_id = request.env['product.attribute'].sudo().search([('name','like','%SIZE%')]).id
        # print('attribute_id',attribute_id)
        if attribute_id:
            query = request._cr.execute("""
                             select pdt_temp.id,pdt_temp.name,pdt_temp.content,pdt_temp.dimensions,pdt_pdt.barcode,
            pdt_temp.list_price,pdt_att.name AS attribute_name,pdt_att_val.name AS attribute_value  from product_template As pdt_temp 
            left join product_product AS pdt_pdt on pdt_temp.id=pdt_pdt.product_tmpl_id
            left join product_template_attribute_line AS pdt_att_line on pdt_temp.id=pdt_att_line.product_tmpl_id
            left join product_attribute AS pdt_att on pdt_att.id=pdt_att_line.attribute_id
            left join product_attribute_value AS pdt_att_val on pdt_att.id=pdt_att_val.attribute_id
            WHERE pdt_att.id = %s and pdt_temp.id in %s """, (attribute_id, tuple([product_id]),))
            res = request._cr.dictfetchall()
            print('res', res)
            res_dumps = json.dumps(res)
            print('res_dumps', res_dumps)
            return res_dumps
            return json.loads({'result': res_dumps})
        else:
            return "Missing Size"

