from odoo import models, fields


class ReportPartnerLedgerInherit(models.AbstractModel):
    _inherit = 'report.accounting_pdf_reports.report_partnerledger'


    def _lines(self, data, partner):
        full_account = super()._lines(data, partner)
        move_line_obj = self.env['account.move.line']

        for r in full_account:
            aml = move_line_obj.browse(r['id'])
            move = aml.move_id
            payment = aml.payment_id

            if payment:
                r['line_type'] = 'payment'
                r['mop'] = payment.journal_id.name or ''
                r['reference_no'] = payment.name or ''
                r['reference_date'] = payment.date or ''
            else:
                r['line_type'] = 'invoice'
                r['invoice_lines'] = [
                    {
                        'product_name': l.product_id.display_name or l.name or '',
                        'qty': l.quantity,
                        'price': l.price_unit,
                        'amount': l.price_subtotal,
                    }
                    for l in move.invoice_line_ids
                    if l.display_type == 'product' or (not l.display_type and l.product_id)
                ]

        return full_account

class AccountPartnerLedger(models.TransientModel):
    _inherit = "account.report.partner.ledger"

    partner_type = fields.Selection(
        [('customer', 'Customer'), ('supplier', 'Vendor')],
        default=lambda self: self.env.context.get('partner_type'))

    def _get_report_data(self, data):
        data = super()._get_report_data(data)
        if self.partner_type:
            rank = 'customer_rank' if self.partner_type == 'customer' else 'supplier_rank'
            partners = self.env['res.partner'].search([(rank, '>', 0)])
            selected = data['form'].get('partner_ids')
            if selected:
                partners = partners.filtered(lambda p: p.id in selected)
            data['form']['partner_ids'] = partners.ids or [0]
        return data