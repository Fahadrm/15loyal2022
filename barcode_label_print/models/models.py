# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from odoo import fields, models,_,api
from odoo.exceptions import UserError
from datetime import date




class BarcodeProductLabelLayout(models.TransientModel):
    _name = 'product.labels'

    print_format = fields.Selection([
        ('label1', 'Big Print'),
        ('label2', 'Small Print'),
        ('label3', 'DTC'),
        ], string="Format", default='label1', required=True)
    custom_quantity = fields.Integer('Quantity', default=1, required=True)
    product_id = fields.Many2one('product.product',required=True)
    product_tmpl_id = fields.Many2one('product.template')
    extra_html = fields.Html('Extra Content', default='')
    rows = fields.Integer(compute='_compute_dimensions')
    columns = fields.Integer(compute='_compute_dimensions')
    product_template_attribute_value_ids = fields.Many2one('product.template.attribute.value', relation='product_variant_combination', string="Attribute Values",required=True)
    categ_id = fields.Many2one('product.category', 'Product Category')
    sub_categ_id = fields.Many2one('product.category', 'Sub Product Category')
    dimensions = fields.Char(string='Dimensions')
    content = fields.Char(string='Content')
    date = fields.Date(string='Date', default=date.today())

    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist')

    sale_price = fields.Float(string ='Price',compute='_compute_price',readonly=False,digits='Product Price',)

    label1_state = fields.Selection([
        ('KL', 'Kerala'),
        ('TM', 'Tamil Nadu,Karnataka & Pondicherry'),
        ('AN', 'Andhrapradesh & Telagana'),
        ('MH', 'Maharashtra,Chattisgarh,Madhya Pradesh & GOA'),
        ('GJ', 'Gujarat'),
        ('RJ', 'Rajasthan'),
        ('UP', 'Uttar Pradesh'),
        ('PB', 'Punjab'),
        ('DL', 'Delhi,Haryana,Jammu and Kashmir,Himachal Pradesh,Chandigarh and Uttaranchal'),
        ('WB', 'Orissa,Bihar,Jharkhand and West Bengal'),
        ('AR', 'Nagaland,Assam,Meghalaya,Arunachal Pradesh,Manipur,Mizoram,Sikkim And Tripura'),
    ], string="State", default='KL')
    label2_state = fields.Selection([
        ('KL', 'Kerala'),
        ('TM', 'Tamil Nadu & Pondicherry'),
        ('AN', 'Andhrapradesh & Telagana'),
        ('KA', 'Karnataka'),
        ('GO', 'GOA'),
        ('MH', 'Maharashtra'),
    ], string="State", default='KL')

    manual_print = fields.Selection([
        ('labels', 'Label Print'),
        ('manual', 'Manual Print'),
    ], string="Manual Print",default='labels')

    serial_no = fields.Char(string='Serial Number')


    @api.depends('product_id','pricelist_id')
    def _compute_price(self):
        self.price_list_price()
        return


    def price_list_price(self):
        lines = []
        for i in self:
            if i.product_id and i.pricelist_id:
                query='''
                select fixed_price from 
                product_pricelist_item where 
                pricelist_id=%s and product_id=%s
                '''
                self.env.cr.execute(query, (
                    i.pricelist_id.id,i.product_id.id
                ))
                for row in self.env.cr.dictfetchall():
                    fixed_price = row['fixed_price'] if row['fixed_price'] else 0.0
                    res = {
                        'fixed_price':fixed_price
                    }
                    lines.append(res)
            if lines:
                i.sale_price = lines[0]['fixed_price']
                return i.sale_price
            else:
                return 0

    @api.onchange('manual_print')
    def _onchange_manual_print(self):
        for i in self:
            i.custom_quantity = 1

    @api.onchange('product_id')
    def _onchange_product(self):
        for i in self:
            if i.product_id:
                i.dimensions=i.product_id.dimensions
                i.content = i.product_id.content
                i.categ_id =i.product_id.categ_id


    @api.depends('print_format')
    def _compute_dimensions(self):
        for wizard in self:
            if 'x' in wizard.print_format:
                columns, rows = wizard.print_format.split('x')[:2]
                wizard.columns = int(columns)
                wizard.rows = int(rows)
            else:
                wizard.columns, wizard.rows = 1, 1



    def _prepare_report_data(self):
        if self.custom_quantity <= 0:
            raise UserError(_('You need to set a positive quantity.'))

        # Get layout grid
        if self.print_format == 'label1':
            xml_id = 'barcode_label_print.report_product_label1'
        elif self.print_format =='label2':
            xml_id = 'barcode_label_print.report_product_label2'
        elif self.print_format =='label3':
            xml_id = 'barcode_label_print.report_product_label3'
        else:
            xml_id = ''

        active_model = ''
        products = self.ids
        active_model = 'product.labels'

        # Build data to pass to the report
        data = {
            'active_model': active_model,
            'quantity_by_product': {p: self.custom_quantity for p in products},
            'layout_wizard': self.id,
            'price_included': 'xprice' in self.print_format,
            'print_format':self.print_format
        }
        return xml_id, data

    # if self.picking_quantity == 'picking' and self.move_line_ids:
    #     qties = defaultdict(int)
    #     custom_barcodes = defaultdict(list)
    #     uom_unit = self.env.ref('uom.product_uom_categ_unit', raise_if_not_found=False)
    #     for line in self.move_line_ids:
    #         if line.product_uom_id.category_id == uom_unit:
    #             if (line.lot_id or line.lot_name) and int(line.qty_done):
    #                 custom_barcodes[line.product_id.id].append((line.lot_id.name or line.lot_name, int(line.qty_done)))
    #                 continue
    #             qties[line.product_id.id] += line.qty_done
    #     # Pass only products with some quantity done to the report
    #     data['quantity_by_product'] = {p: int(q) for p, q in qties.items() if q}
    #     data['custom_barcodes'] = custom_barcodes



    def serial_updation(self,serials):
        for i in self:
            i.product_id.serial_no = serials
        return


    def process(self):
        self.ensure_one()
        xml_id, data = self._prepare_report_data()
        if not xml_id:
            raise UserError(_('Unable to find report template for %s format', self.print_format))
        return self.env.ref(xml_id).report_action(None, data=data)

