# -*- coding: utf-8 -*-
# Part of ESFSM Report. See LICENSE file for full copyright and licensing details.

from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install', 'esfsm_report')
class TestEsfsmReport(TransactionCase):
    """Test suite for ESFSM Report module"""

    @classmethod
    def setUpClass(cls):
        """Set up test data"""
        super().setUpClass()

        # Create test partner
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'street': 'Test Street 123',
            'city': 'Test City',
            'phone': '+389 75 123 456',
            'email': 'test@example.com',
        })

        # Create test employee
        cls.employee = cls.env['hr.employee'].create({
            'name': 'Test Technician',
            'mobile_phone': '+389 70 987 654',
        })

        # Create test team
        cls.team = cls.env['esfsm.team'].create({
            'name': 'Test Team',
            'member_ids': [(4, cls.employee.id)],
        })

        # Create test stage
        cls.stage = cls.env['esfsm.job.stage'].create({
            'name': 'In Progress',
            'sequence': 10,
        })

        # Create test job type
        cls.job_type = cls.env['esfsm.job.type'].create({
            'name': 'Installation',
        })

        # Create test job
        cls.job = cls.env['esfsm.job'].create({
            'partner_id': cls.partner.id,
            'employee_ids': [(6, 0, [cls.employee.id])],
            'stage_id': cls.stage.id,
            'job_type_id': cls.job_type.id,
            'scheduled_date_start': '2025-11-25 10:00:00',
            'scheduled_date_end': '2025-11-25 14:00:00',
            'description': 'Test job description',
        })

    def test_01_report_action_exists(self):
        """Test that Work Order report action exists"""
        report = self.env.ref('esfsm_report.action_report_esfsm_work_order', raise_if_not_found=False)
        self.assertTrue(report, "Work Order report action should exist")
        self.assertEqual(report.model, 'esfsm.job')
        self.assertEqual(report.report_type, 'qweb-pdf')

    def test_02_action_print_work_order(self):
        """Test action_print_work_order method"""
        action = self.job.action_print_work_order()

        self.assertEqual(action['type'], 'ir.actions.report')
        self.assertIn('report_name', action)

    def test_03_report_rendering_basic(self):
        """Test basic report rendering without optional modules"""
        report = self.env.ref('esfsm_report.action_report_esfsm_work_order')

        # Render HTML version for testing
        html = report._render_qweb_html([self.job.id])[0]

        self.assertIn(self.job.name.encode(), html)
        self.assertIn(self.partner.name.encode(), html)
        self.assertIn(self.employee.name.encode(), html)
        self.assertIn('РАБОТЕН НАЛОГ'.encode('utf-8'), html)

    def test_04_has_stock_module(self):
        """Test _has_stock_module method"""
        # Should return True if esfsm_stock is installed
        has_stock = self.job._has_stock_module()
        self.assertIsInstance(has_stock, bool)

    def test_05_has_timesheet_module(self):
        """Test _has_timesheet_module method"""
        # Should return True if esfsm_timesheet is installed
        has_timesheet = self.job._has_timesheet_module()
        self.assertIsInstance(has_timesheet, bool)

    def test_06_duration_display(self):
        """Test duration display methods"""
        # Set actual duration
        self.job.write({
            'date_start': '2025-11-25 10:00:00',
            'date_end': '2025-11-25 13:30:00',
        })

        duration_display = self.job._get_duration_display()
        self.assertIn('ч', duration_display)  # Should contain hours

        scheduled_display = self.job._get_scheduled_duration_display()
        self.assertIn('ч', scheduled_display)

    def test_07_report_with_checklist(self):
        """Test report rendering with checklist items"""
        # Add checklist items
        self.env['esfsm.job.checklist'].create({
            'job_id': self.job.id,
            'name': 'Task 1',
            'done': True,
            'sequence': 1,
        })
        self.env['esfsm.job.checklist'].create({
            'job_id': self.job.id,
            'name': 'Task 2',
            'done': False,
            'sequence': 2,
            'notes': 'Important note',
        })

        report = self.env.ref('esfsm_report.action_report_esfsm_work_order')
        html = report._render_qweb_html([self.job.id])[0]

        self.assertIn(b'Task 1', html)
        self.assertIn(b'Task 2', html)
        self.assertIn('Checklist'.encode('utf-8'), html)

    def test_08_report_with_team(self):
        """Test report rendering with team instead of individual technician"""
        job_with_team = self.env['esfsm.job'].create({
            'partner_id': self.partner.id,
            'team_id': self.team.id,
            'scheduled_date_start': '2025-11-26 09:00:00',
        })

        report = self.env.ref('esfsm_report.action_report_esfsm_work_order')
        html = report._render_qweb_html([job_with_team.id])[0]

        self.assertIn(self.team.name.encode(), html)
        self.assertIn(self.employee.name.encode(), html)  # Team member

    def test_09_report_filename(self):
        """Test report filename generation"""
        report = self.env.ref('esfsm_report.action_report_esfsm_work_order')

        # The print_report_name should include job name
        self.assertIn('object.name', report.print_report_name)

    def test_10_report_with_signatures(self):
        """Test report rendering with signatures"""
        import base64

        # Create a minimal 1x1 pixel transparent PNG
        minimal_png = base64.b64encode(
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
            b'\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
            b'\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01'
            b'\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        )

        self.job.write({
            'technician_signature': minimal_png,
            'technician_signature_date': '2025-11-25',
            'customer_signature': minimal_png,
            'customer_signature_date': '2025-11-25',
        })

        report = self.env.ref('esfsm_report.action_report_esfsm_work_order')
        html = report._render_qweb_html([self.job.id])[0]

        self.assertIn(b'data:image/png;base64', html)
        self.assertIn('Потпис на техничар'.encode('utf-8'), html)
        self.assertIn('Потпис на клиент'.encode('utf-8'), html)

    def test_11_report_with_priority(self):
        """Test report rendering with different priority levels"""
        for priority in ['0', '1', '2', '3']:
            job = self.env['esfsm.job'].create({
                'partner_id': self.partner.id,
                'employee_ids': [(6, 0, [self.employee.id])],
                'priority': priority,
                'scheduled_date_start': '2025-11-27 10:00:00',
            })

            report = self.env.ref('esfsm_report.action_report_esfsm_work_order')
            html = report._render_qweb_html([job.id])[0]

            self.assertIn('Приоритет'.encode('utf-8'), html)

    def test_12_report_multicompany(self):
        """Test report rendering with company logo and info"""
        self.job.company_id.write({
            'phone': '+389 2 123 4567',
            'email': 'info@company.com',
        })

        report = self.env.ref('esfsm_report.action_report_esfsm_work_order')
        html = report._render_qweb_html([self.job.id])[0]

        self.assertIn(self.job.company_id.phone.encode(), html)
        self.assertIn(self.job.company_id.email.encode(), html)
