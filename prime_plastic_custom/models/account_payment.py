# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    is_payment_receipt_printed = fields.Boolean(
        string='Payment Receipt Printed',
        default=False,
        copy=False,
    )

    invoice_ids = fields.Many2one(
        'account.move',
        string='Invoice',
        domain="[('partner_id','=',partner_id),"
               "('state','=','posted'),"
               "('payment_state','not in',['paid','in_payment']),"
               "('move_type','in',['out_invoice','in_invoice','out_refund','in_refund'])]"
    )

    def write(self, vals):
        res = super().write(vals)
        if vals.get('state') == 'paid':
            for payment in self:
                payment._auto_reconcile_selected_invoices()
        return res

    def _auto_reconcile_selected_invoices(self):
        self.ensure_one()

        invoice = self.invoice_ids
        if not invoice:
            return

        if invoice.payment_state in ('paid', 'in_payment'):
            return

        # Payment's outstanding receivable/payable line
        payment_lines = self.move_id.line_ids.filtered(
            lambda l: l.account_id.account_type in (
                'asset_receivable',
                'liability_payable',
            ) and not l.reconciled
        )
        if not payment_lines:
            return

        invoice_lines = invoice.line_ids.filtered(
            lambda l: l.account_id.account_type in (
                'asset_receivable',
                'liability_payable',
            )
            and not l.reconciled
            and l.account_id == payment_lines[:1].account_id
        )
        if not invoice_lines:
            return

        try:
            (payment_lines + invoice_lines).reconcile()
        except Exception:
            # Skip silently if reconciliation is not possible
            pass