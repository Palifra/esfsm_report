# -*- coding: utf-8 -*-
# Part of ESFSM Report. See LICENSE file for full copyright and licensing details.

from odoo import models


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _run_wkhtmltopdf(
        self,
        bodies,
        report_ref=False,
        header=None,
        footer=None,
        landscape=False,
        specific_paperformat_args=None,
        set_viewport_size=False,
    ):
        """Override to add custom footer with page numbering for ESFSM reports."""

        # Check if this is our report
        # report_ref can be string or ir.actions.report recordset
        report_name = report_ref if isinstance(report_ref, str) else (report_ref.report_name if report_ref else '')
        if report_name == 'esfsm_report.report_work_order_document':
            footer = '''<!DOCTYPE html>
<html><head><meta charset="utf-8"/>
<style>body{font-family:Arial,sans-serif;font-size:7pt;color:#666;margin:0;padding:2px 10px;}
.f{text-align:center;border-top:1px solid #ddd;padding-top:2px;}</style></head>
<body><div class="f">Автоматски генериран документ од ESFSM системот | Тел: +389 34 612 263 | Email: eskon@eskon.com.mk | Страна <span id="p"></span>/<span id="t"></span></div>
<script>var v={},q=document.location.search.substring(1).split("&");for(var i=0;i<q.length;i++){var p=q[i].split("=",2);v[p[0]]=decodeURIComponent(p[1]||"");}
document.getElementById("p").textContent=v["page"]||"";document.getElementById("t").textContent=v["topage"]||"";</script></body></html>'''

        return super()._run_wkhtmltopdf(
            bodies,
            report_ref=report_ref,
            header=header,
            footer=footer,
            landscape=landscape,
            specific_paperformat_args=specific_paperformat_args,
            set_viewport_size=set_viewport_size,
        )
