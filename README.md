# ESFSM - Работен налог (Work Order Report)

Професионален PDF извештај за теренски работи.

## Опис

Овој модул додава "Работен налог" - професионален QWeb PDF извештај за теренските работи во ESFSM системот. Работниот налог е комплетен документ кој ги содржи сите детали за работата, користените материјали, потрошените часови, чеклисти и потписи од техничар и клиент.

## Главни Карактеристики

### 📄 Професионален PDF Извештај
- **Комплетен работен налог**: Сите детали на една страна
- **Компаниско брендирање**: Лого, контакт информации
- **Македонски јазик**: Целосно на македонски
- **Печатење и е-пошта**: Директно печатење или испраќање како прилог

### 📋 Содржина на извештајот

**1. Header секција:**
- Лого на компанијата
- Наслов: "РАБОТЕН НАЛОГ"
- Контакт информации

**2. Основни информации:**
- Број на работа (FSM-XXXX)
- Датум на креирање
- Статус/етапа
- Приоритет
- Тип на работа

**3. Клиент и локација:**
- Име на клиент, телефон, е-пошта
- Адреса на клиент
- Локација на сервисирање

**4. Техничар/Тим:**
- Назначен техничар или тим
- Мобилен телефон
- Членови на тимот (ако е тим)
- Планирано vs. вкупно траење

**5. Опис на работата:**
- Детален опис
- Забелешки

**6. Checklist** (ако постои):
- Табела со задачи
- Статус индикатори (✓/☐)
- Прогрес бар
- Забелешки по задача

**7. Материјали** (ако е инсталиран esfsm_stock):
- Земено количество
- Искористено количество
- Вратено количество
- Единична мера
- Цена и вкупен износ

**8. Времиња** (ако е инсталиран esfsm_timesheet):
- Датум
- Вработен
- Опис
- Часови (float_time формат)
- Вкупно часови

**9. Потписи:**
- Потпис на техничар + датум
- Потпис на клиент + датум

**10. Footer:**
- Автоматски генериран текст
- Контакт информации

## Технички Детали

### Зависности
- `esfsm` (задолжително) - Core FSM модул

### Опционални Интеграции
- `esfsm_stock` - Прикажува користени материјали
- `esfsm_timesheet` - Прикажува времиња

### Додадени Методи на `esfsm.job`

#### `action_print_work_order()`
Отвора дијалог за печатење на работен налог.

```python
job.action_print_work_order()
```

#### `_has_stock_module()`
Проверува дали е инсталиран esfsm_stock модул.

```python
if job._has_stock_module():
    # Прикажи материјали
```

#### `_has_timesheet_module()`
Проверува дали е инсталиран esfsm_timesheet модул.

```python
if job._has_timesheet_module():
    # Прикажи времиња
```

#### `_get_duration_display()`
Форматира траење за приказ (пр. "3ч 30мин").

```python
duration = job._get_duration_display()
# Output: "3ч 30мин"
```

#### `_get_scheduled_duration_display()`
Форматира планирано траење за приказ.

```python
scheduled = job._get_scheduled_duration_display()
# Output: "4ч"
```

## Инсталација

### Развојна Околина

```bash
# Активирај dev mode
./odoo-bin --dev=all -d your_database -u esfsm_report

# Или инсталирај нов модул
./odoo-bin -d your_database -i esfsm_report --stop-after-init
```

### Docker (Production)

```bash
# Ажурирај листа на модули
docker exec -i odoo_server odoo shell -d eskon --no-http << 'EOF'
env['ir.module.module'].update_list()
env.cr.commit()
EOF

# Инсталирај модул
docker exec -i odoo_server odoo shell -d eskon --no-http << 'EOF'
module = env['ir.module.module'].search([('name', '=', 'esfsm_report')])
if module.state == 'uninstalled':
    module.button_immediate_install()
    env.cr.commit()
    print("Модулот е инсталиран!")
EOF

# Рестартирај Odoo
docker restart odoo_server
```

### Верификација

```bash
# Провери статус на модул
docker exec -i odoo_server odoo shell -d eskon --no-http << 'EOF'
module = env['ir.module.module'].search([('name', '=', 'esfsm_report')])
print(f"Модул: {module.name}, Состојба: {module.state}")
EOF
```

## Користење

### Печатење на Работен налог

#### Метод 1: Од формата на работата

1. Отворете работа
2. Кликнете на копчето **"Печати Работен налог"** во header
3. PDF ќе се генерира и отвори во нова табла

#### Метод 2: Од Print менито

1. Отворете работа
2. Кликнете на **Print**
3. Изберете **"Работен налог"**

#### Метод 3: Програмски

```python
# Генерирај работен налог за работа
job = env['esfsm.job'].browse(123)
action = job.action_print_work_order()
```

### Испраќање по Е-пошта

1. Отворете работа
2. Кликнете на **Send by Email**
3. "Работен налог" ќе биде автоматски прикачен како PDF

### Bulk Печатење

```python
# Печати повеќе работни налози одеднаш
jobs = env['esfsm.job'].search([('stage_id.done', '=', True)])
report = env.ref('esfsm_report.action_report_esfsm_work_order')
report.report_action(jobs)
```

## Примери

### Генерирање на PDF

```python
# Пронајди работа
job = env['esfsm.job'].search([('name', '=', 'FSM-001')], limit=1)

# Генерирај PDF
report = env.ref('esfsm_report.action_report_esfsm_work_order')
pdf_content, file_type = report._render_qweb_pdf([job.id])

# Зачувај PDF
import base64
attachment = env['ir.attachment'].create({
    'name': f'Работен налог - {job.name}.pdf',
    'type': 'binary',
    'datas': base64.b64encode(pdf_content),
    'res_model': 'esfsm.job',
    'res_id': job.id,
    'mimetype': 'application/pdf',
})
```

### Прикажи HTML Верзија (за дебаг)

```python
# Генерирај HTML верзија на извештајот
job = env['esfsm.job'].browse(123)
report = env.ref('esfsm_report.action_report_esfsm_work_order')
html_content = report._render_qweb_html([job.id])[0]

# Зачувај во фајл за преглед
with open('/tmp/work_order.html', 'wb') as f:
    f.write(html_content)
```

### Масовно Печатење со Филтри

```python
# Печати сите завршени работи од овој месец
from datetime import datetime, timedelta

start_of_month = datetime.now().replace(day=1)
jobs = env['esfsm.job'].search([
    ('date_end', '>=', start_of_month),
    ('stage_id.done', '=', True),
])

print(f"Генерирам {len(jobs)} работни налози...")
report = env.ref('esfsm_report.action_report_esfsm_work_order')
pdf_content = report._render_qweb_pdf(jobs.ids)[0]

# Зачувај како еден PDF
with open('/tmp/monthly_reports.pdf', 'wb') as f:
    f.write(pdf_content)
```

## Тестирање

Модулот вклучува 12 комплетни тест-случаеви:

```bash
# Врти сите тестови
./odoo-bin -d test_db --test-enable --test-tags=/esfsm_report --stop-after-init

# Врти специфичен тест
./odoo-bin -d test_db --test-enable \
  --test-tags=/esfsm_report.TestEsfsmReport.test_03_report_rendering_basic
```

### Тест Покриеност

- ✅ Постоење на report action
- ✅ Генерирање на PDF
- ✅ Rendering со checklist
- ✅ Rendering со тим (наместо техничар)
- ✅ Rendering со потписи
- ✅ Rendering со приоритети
- ✅ Multi-company поддршка
- ✅ Опционални модули (stock, timesheet)
- ✅ Duration formatting
- ✅ Filename генерирање

## Архитектура

### QWeb Template Структура

```xml
<template id="report_work_order_document">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="o">
            <t t-call="web.external_layout">
                <div class="page">
                    <!-- Header -->
                    <!-- Job Information -->
                    <!-- Customer & Location -->
                    <!-- Technician/Team -->
                    <!-- Description -->
                    <!-- Checklist (if exists) -->
                    <!-- Materials (if esfsm_stock) -->
                    <!-- Timesheets (if esfsm_timesheet) -->
                    <!-- Signatures -->
                    <!-- Footer -->
                </div>
            </t>
        </t>
    </t>
</template>
```

### Условна Логика

```xml
<!-- Прикажи материјали само ако е инсталиран esfsm_stock -->
<t t-if="o._has_stock_module() and o.material_ids">
    <div>
        <!-- Materials table -->
    </div>
</t>

<!-- Прикажи времиња само ако е инсталиран esfsm_timesheet -->
<t t-if="o._has_timesheet_module() and o.timesheet_ids">
    <div>
        <!-- Timesheets table -->
    </div>
</t>
```

## Проблеми и Решенија

### Проблем: PDF не се генерира

**Решение:**
1. Провери дали wkhtmltopdf е инсталиран:
   ```bash
   docker exec odoo_server which wkhtmltopdf
   ```
2. Провери логови:
   ```bash
   docker logs odoo_server --tail 100 | grep -i wkhtmltopdf
   ```

### Проблем: Празен PDF или грешка во rendering

**Решение:**
1. Тестирај HTML верзија:
   ```python
   report = env.ref('esfsm_report.action_report_esfsm_work_order')
   html = report._render_qweb_html([job.id])[0]
   # Провери за грешки во HTML
   ```
2. Провери дали има encoding проблеми со македонски карактери

### Проблем: Потписите не се прикажуваат

**Решение:**
1. Провери дали signature полињата се пополнети:
   ```python
   job = env['esfsm.job'].browse(123)
   print(f"Technician signature: {bool(job.technician_signature)}")
   print(f"Customer signature: {bool(job.customer_signature)}")
   ```
2. Провери дали base64 encoding е валиден

### Проблем: Материјали/Времиња не се прикажуваат

**Решение:**
- Провери дали соодветните модули се инсталирани:
  ```python
  job = env['esfsm.job'].browse(123)
  print(f"Has stock: {job._has_stock_module()}")
  print(f"Has timesheet: {job._has_timesheet_module()}")
  ```

## Поврзани Модули

### ESFSM Екосистем

- **[esfsm](https://github.com/Palifra/esfsm)** - Core Field Service Management
- **[esfsm_project](https://github.com/Palifra/esfsm_project)** - Project Integration
- **[esfsm_stock](https://github.com/Palifra/esfsm_stock)** - Stock & Material Tracking
- **[esfsm_timesheet](https://github.com/Palifra/esfsm_timesheet)** - Timesheet Integration
- **[esfsm_helpdesk]** - Helpdesk Integration (Coming soon)
- **[esfsm_maintenance]** - Equipment Maintenance (Coming soon)

## Развој

### Структура на Модулот

```
esfsm_report/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── esfsm_job.py
├── report/
│   ├── esfsm_work_order_report.xml
│   └── esfsm_work_order_templates.xml
├── security/
│   └── ir.model.access.csv
├── tests/
│   ├── __init__.py
│   └── test_esfsm_report.py
└── views/
    └── esfsm_job_views.xml
```

### Додавање Нови Секции во Извештајот

Пример: Додади "Equipment" секција:

```xml
<!-- Во esfsm_work_order_templates.xml -->
<div t-if="o.equipment_id" style="margin-bottom: 25px;">
    <h5 style="color: #2c3e50; margin-bottom: 10px;">
        <i class="fa fa-cog"/> Опрема
    </h5>
    <table class="table table-sm">
        <tr>
            <td><strong>Модел:</strong></td>
            <td><span t-field="o.equipment_id.name"/></td>
        </tr>
        <tr>
            <td><strong>Сериски број:</strong></td>
            <td><span t-field="o.equipment_id.serial_no"/></td>
        </tr>
    </table>
</div>
```

### Прилагодување на Стилови

```xml
<!-- Додади custom CSS -->
<template id="custom_report_styles" inherit_id="web.report_layout">
    <xpath expr="//head" position="inside">
        <style>
            .custom-header {
                background-color: #your-color;
            }
        </style>
    </xpath>
</template>
```

## Лиценца

LGPL-3

## Автор

**ЕСКОН-ИНЖЕНЕРИНГ ДООЕЛ Струмица**

- **Email:** info@eskon.com.mk
- **Website:** https://www.eskon.com.mk
- **GitHub:** https://github.com/Palifra

## Верзија

**18.0.1.0.0** - Одоо 18 Community Edition

---

**Последно ажурирано:** 2025-11-23
