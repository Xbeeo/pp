from datetime import datetime, time, timedelta
from odoo import models, fields


class OutsourcedLedgerWizard(models.TransientModel):
    _name = 'outsourced.ledger.wizard'
    _description = 'Outsourced Production Item Ledger'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    product_id = fields.Many2one('product.product', string='Product')

    def action_print(self):
        return self.env.ref('prime_plastic_report.action_ledger_report').report_action(self)

    def _get_printed_on(self):
        return fields.Datetime.context_timestamp(self, fields.Datetime.now()).strftime('%d-%b-%Y %H:%M')

    def _get_raw(self, date_domain):
        domain = date_domain + [('state', 'in', ['purchase', 'done'])]
        if self.partner_id:
            domain.append(('partner_id', '=', self.partner_id.id))
        if self.product_id:
            domain.append(('order_line.product_id', '=', self.product_id.id))
        raw = []  # (date, id, product, w_out, pcs, rate, stock_weight)
        for po in self.env['purchase.order'].search(domain, order='date_order, id'):
            lines = po.order_line.filtered(lambda x: not x.display_type and x.product_id and (
                    not self.product_id or x.product_id == self.product_id))
            if not lines:
                continue
            for m in po._get_subcontracting_resupplies().move_ids.filtered(lambda m: m.state == 'done'):
                raw.append((m.date, m.id, m.product_id, m.quantity, 0.0, None, None))
            for l in lines:
                for m in l.move_ids.filtered(lambda m: m.state == 'done'
                                                       and m.picking_id.picking_type_id.code == 'incoming'):
                    raw.append((m.date, m.id, l.product_id, 0.0, m.quantity,
                                l.price_unit, l.receiving_weight))
        raw.sort(key=lambda r: (r[0], r[1]))
        return raw

    def _get_lines(self):
        self.ensure_one()
        start = datetime.combine(self.date_from, time.min)
        end = datetime.combine(self.date_to, time.min) + timedelta(days=1)
        f2 = '{:,.2f}'.format

        # opening balance: everything before date_from
        opening = 0.0
        for _d, _i, _p, w_out, pcs, _r, sw in self._get_raw([('date_order', '<', start)]):
            opening += w_out - pcs * (sw or 0.0)

        raw = self._get_raw([('date_order', '>=', start), ('date_order', '<', end)])
        rows, balance = [], opening
        t_out = t_in = t_prod = 0.0
        for dt, _id, p, w_out, pcs, rate, sw in raw:
            prod_w = pcs * (sw or 0.0)
            balance += w_out - prod_w
            t_out += w_out
            t_in += pcs
            t_prod += prod_w
            rows.append({
                'sr': len(rows) + 1,
                'date': dt.strftime('%d-%b-%Y'),
                'desc': p.display_name,
                'color': p.product_color_id.name or '',
                'model': p.product_model_id.name or '',
                'weight_out': f2(w_out) if w_out else '',
                'pcs_in': f2(pcs) if pcs else '',
                'rate': f2(rate) if rate is not None else '',
                'stock_weight': f2(sw) if sw is not None else '',
                'prod_weight_in': f2(prod_w) if pcs else '',
                'pre_weight': f2(balance),
            })
        totals = {'opening': f2(opening), 'weight_out': f2(t_out), 'pcs_in': f2(t_in),
                  'prod_weight_in': f2(t_prod), 'pre_weight': f2(balance)}
        return rows, totals