from datetime import date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DiscountLimit(models.TransientModel):
    _inherit = 'res.config.settings'

    discount_limit = fields.Boolean(string='Discount Limit')
    discount_limit_amount = fields.Float(string='Maximum Discount', default=10.0)

    @api.model
    def get_values(self):
        res = super(DiscountLimit, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            discount_limit=get_param('res.config.settings.discount_limit'),
            discount_limit_amount=get_param('res.config.settings.discount_limit_amount'),
        )
        return res

    def set_values(self):
        res = super(DiscountLimit, self).get_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        res.update(
            discount_limit=set_param('res.config.settings.discount_limit', self.discount_limit),
            discount_limit_amount=set_param('res.config.settings.discount_limit_amount', self.discount_limit_amount),
        )
        return res


class DiscountLimitSale(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(DiscountLimitSale, self).action_confirm()

        current_month = date.today().month
        print(current_month, 'sssss')
        search = self.search([])

        total_discount = sum(order.order_line.discount for order in search if order.date_order.month == current_month)
        print(total_discount)

        discount_limit_conf_settings = self.env['ir.config_parameter'].sudo().get_param(
            'res.config.settings.discount_limit_amount')

        discount_limit_amount_conf_settings = self.env['ir.config_parameter'].get_param(
            'res.config.settings.discount_limit')

        print(discount_limit_amount_conf_settings)

        if discount_limit_amount_conf_settings:

            if total_discount > float(discount_limit_conf_settings):
                
                raise ValidationError(_("Total discount for the current month exceeds the limit"))
        return res
