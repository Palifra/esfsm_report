# -*- coding: utf-8 -*-
# Part of ESFSM Report. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EsfsmJob(models.Model):
    _inherit = 'esfsm.job'

    def action_print_work_order(self):
        """Print Work Order (Работен налог) report"""
        self.ensure_one()
        return self.env.ref('esfsm_report.action_report_esfsm_work_order').report_action(self)

    @api.model
    def _has_stock_module(self):
        """Check if esfsm_stock module is installed"""
        return 'material_ids' in self.env['esfsm.job']._fields

    @api.model
    def _has_timesheet_module(self):
        """Check if esfsm_timesheet module is installed"""
        return 'timesheet_ids' in self.env['esfsm.job']._fields

    def _get_duration_display(self):
        """Get formatted duration for display"""
        self.ensure_one()
        if self.duration:
            hours = int(self.duration)
            minutes = int((self.duration - hours) * 60)
            if minutes:
                return f"{hours}ч {minutes}мин"
            return f"{hours}ч"
        return "-"

    def _get_scheduled_duration_display(self):
        """Get formatted scheduled duration for display"""
        self.ensure_one()
        if self.scheduled_duration:
            hours = int(self.scheduled_duration)
            minutes = int((self.scheduled_duration - hours) * 60)
            if minutes:
                return f"{hours}ч {minutes}мин"
            return f"{hours}ч"
        return "-"
