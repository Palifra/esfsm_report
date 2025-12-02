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
        """Get formatted actual duration for display.

        Uses total_hours from timesheets if esfsm_timesheet is installed,
        otherwise calculates from date_start/date_end timestamps.
        """
        self.ensure_one()
        duration = 0.0

        # Prefer total_hours from timesheets if available
        if self._has_timesheet_module() and hasattr(self, 'total_hours'):
            duration = self.total_hours
        # Fallback: calculate from timestamps
        elif self.date_start and self.date_end:
            delta = self.date_end - self.date_start
            duration = delta.total_seconds() / 3600.0

        if duration:
            hours = int(duration)
            minutes = int((duration - hours) * 60)
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

    def _get_materials_for_report(self, min_rows=15):
        """Return materials with empty rows to fill minimum rows for manual entry.

        Args:
            min_rows: Minimum number of rows to return (default 15)

        Returns:
            List of dicts with material data or empty placeholders
        """
        self.ensure_one()
        materials = []

        # Add existing materials if esfsm_stock is installed
        if self._has_stock_module() and self.material_ids:
            for material in self.material_ids:
                materials.append({
                    'product_name': material.product_id.name if material.product_id else '',
                    'taken_qty': material.taken_qty,
                    'used_qty': material.used_qty,
                    'returned_qty': material.returned_qty,
                    'uom_name': material.product_uom_id.name if material.product_uom_id else '',
                    'is_empty': False,
                })

        # Fill remaining rows with empty placeholders
        current_count = len(materials)
        for i in range(current_count, min_rows):
            materials.append({
                'product_name': '',
                'taken_qty': '',
                'used_qty': '',
                'returned_qty': '',
                'uom_name': '',
                'is_empty': True,
            })

        return materials
