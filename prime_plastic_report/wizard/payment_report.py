# -*- coding: utf-8 -*-
from odoo import models


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        result = super()._render_qweb_pdf(report_ref, res_ids=res_ids, data=data)
        report = self._get_report(report_ref)
        if report and report.report_name == 'account.report_payment_receipt' and res_ids:
            payments = self.env['account.payment'].browse(res_ids).filtered(
                lambda p: not p.is_payment_receipt_printed
            )
            if payments:
                payments.write({'is_payment_receipt_printed': True})
        return result