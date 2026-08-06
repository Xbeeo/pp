from odoo import models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends(
        'state', 'currency_id', 'invoice_payments_widget',
    )
    def _compute_payments_widget_to_reconcile_info(self):
        super()._compute_payments_widget_to_reconcile_info()
        for move in self:
            widget_vals = move.invoice_outstanding_credits_debits_widget
            if not widget_vals or not isinstance(widget_vals, dict):
                continue

            content = widget_vals.get('content', [])
            if not content:
                continue

            payments = self.env['account.payment'].search([
                ('state', '=', 'paid'),
                ('invoice_ids', 'in', move.ids),
            ])
            allowed_move_ids = set(payments.move_id.ids)

            filtered_content = [
                c for c in content if c.get('move_id') in allowed_move_ids
            ]

            if filtered_content:
                widget_vals['content'] = filtered_content
                move.invoice_outstanding_credits_debits_widget = widget_vals
            else:
                move.invoice_outstanding_credits_debits_widget = False