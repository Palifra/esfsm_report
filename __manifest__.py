# -*- coding: utf-8 -*-
# Part of ESFSM Report. See LICENSE file for full copyright and licensing details.

{
    'name': 'ESFSM - Работен налог (Report)',
    'version': '18.0.1.0.0',
    'category': 'Services/Field Service',
    'summary': 'Печатење на работен налог за теренски работи',
    'description': """
Field Service Management - Работен налог (Work Order Report)
=============================================================

Овој модул додава професионален PDF извештај "Работен налог" за теренските работи.

Главни карактеристики
---------------------
* **Професионален PDF**: Работен налог со компаниско брендирање
* **Комплетни детали**: Информации за работата, клиент, техничар, локација
* **Checklist**: Преглед на завршени и незавршени задачи
* **Материјали**: Табела со користени материјали (ако е инсталиран esfsm_stock)
* **Времиња**: Преглед на потрошени часови (ако е инсталиран esfsm_timesheet)
* **Двоен потпис**: Простор за потпис на техничар и клиент
* **Македонски јазик**: Целосно на македонски јазик

Функционалности
---------------
* Печатење на работен налог од формата на работата
* Smart button за брз пристап
* Испраќање по е-пошта како прилог
* Автоматска детекција на инсталирани модули
* Мулти-компаниска поддршка со лого

Технички детали
----------------
* QWeb PDF темплејт
* Зависности: esfsm (задолжително)
* Опционални: esfsm_stock, esfsm_timesheet
* Компатибилно со multi-company

    """,
    'author': 'ЕСКОН-ИНЖЕНЕРИНГ ДООЕЛ Струмица',
    'website': 'https://www.eskon.com.mk',
    'license': 'LGPL-3',
    'depends': [
        'esfsm',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Reports
        'report/esfsm_work_order_report.xml',
        'report/esfsm_work_order_templates.xml',

        # Views
        'views/esfsm_job_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
