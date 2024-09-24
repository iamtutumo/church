import frappe
from frappe import _
from datetime import datetime
from dateutil.relativedelta import relativedelta

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    chart = get_chart_data(data, filters)
    summary = get_summary(data)
    return columns, data, None, chart, summary

def get_columns(filters):
    columns = [
        {
            "fieldname": "group_by",
            "label": _(filters.get("group_by", "Month")),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "total_amount",
            "label": _("Total Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "contribution_count",
            "label": _("Contribution Count"),
            "fieldtype": "Int",
            "width": 120
        }
    ]
    
    if filters.get("group_by") == "Contribution Type":
        columns.append({
            "fieldname": "contribution_type",
            "label": _("Contribution Type"),
            "fieldtype": "Link",
            "options": "Contribution Type",
            "width": 180
        })
    
    return columns

def get_data(filters):
    conditions = get_conditions(filters)
    group_by = get_group_by(filters)
    
    data = frappe.db.sql(f"""
        SELECT 
            {group_by} as group_by,
            SUM(amount) as total_amount,
            COUNT(*) as contribution_count
            {', contribution_type' if filters.get('group_by') == 'Contribution Type' else ''}
        FROM `tabChurch Payment`
        WHERE docstatus = 1 {conditions}
        GROUP BY {group_by}
        ORDER BY {group_by}
    """, filters, as_dict=1)

    return data

def get_conditions(filters):
    conditions = []
    if filters.get("from_date"):
        conditions.append("payment_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("payment_date <= %(to_date)s")
    if filters.get("diocese"):
        conditions.append("diocese = %(diocese)s")
    if filters.get("archdeaconry"):
        conditions.append("archdeaconry = %(archdeaconry)s")
    if filters.get("parish"):
        conditions.append("parish = %(parish)s")
    if filters.get("contribution_type"):
        conditions.append("contribution_type = %(contribution_type)s")
    
    return " AND " + " AND ".join(conditions) if conditions else ""

def get_group_by(filters):
    group_by = filters.get("group_by", "Month")
    if group_by == "Month":
        return "DATE_FORMAT(payment_date, '%Y-%m')"
    elif group_by == "Quarter":
        return "CONCAT(YEAR(payment_date), '-Q', QUARTER(payment_date))"
    elif group_by == "Year":
        return "YEAR(payment_date)"
    elif group_by == "Contribution Type":
        return "contribution_type"

def get_chart_data(data, filters):
    labels = [d.group_by for d in data]
    datasets = [{
        'name': _('Total Contributions'),
        'values': [d.total_amount for d in data]
    }]

    chart = {
        'data': {
            'labels': labels,
            'datasets': datasets
        },
        'type': 'line',
        'colors': ['#4CAF50']
    }

    return chart

def get_summary(data):
    total_amount = sum(d.total_amount for d in data)
    total_count = sum(d.contribution_count for d in data)
    avg_contribution = total_amount / total_count if total_count else 0

    return [
        {
            "value": total_amount,
            "label": _("Total Contributions"),
            "datatype": "Currency",
            "currency": frappe.defaults.get_global_default("currency")
        },
        {
            "value": total_count,
            "label": _("Total Number of Contributions"),
            "datatype": "Int"
        },
        {
            "value": avg_contribution,
            "label": _("Average Contribution"),
            "datatype": "Currency",
            "currency": frappe.defaults.get_global_default("currency")
        }
    ]