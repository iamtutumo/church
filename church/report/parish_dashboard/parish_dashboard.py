import frappe
from frappe import _
from datetime import datetime

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    summary = get_summary(data)
    return columns, data, None, chart, summary

def get_columns():
    return [
        {
            "fieldname": "name",
            "label": _("Name"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "type",
            "label": _("Type"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "total_members",
            "label": _("Total Members"),
            "fieldtype": "Int",
            "width": 120
        },
        {
            "fieldname": "total_contributions",
            "label": _("Total Contributions"),
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "fieldname": "avg_contribution_per_member",
            "label": _("Avg Contribution/Member"),
            "fieldtype": "Currency",
            "width": 180
        },
        {
            "fieldname": "last_contribution_date",
            "label": _("Last Contribution Date"),
            "fieldtype": "Date",
            "width": 150
        }
    ]

def get_data(filters):
    data = []
    parishes = get_parishes(filters)
    
    for parish in parishes:
        parish_data = get_entity_data("Parish", parish.name, filters)
        parish_data["parent"] = None
        data.append(parish_data)
        
        sub_parishes = get_sub_parishes(parish.name)
        for sub_parish in sub_parishes:
            sub_parish_data = get_entity_data("Sub Parish", sub_parish.name, filters)
            sub_parish_data["parent"] = parish.name
            data.append(sub_parish_data)

    return data

def get_entity_data(doctype, name, filters):
    total_members = get_total_members(doctype, name)
    total_contributions, last_contribution_date = get_contribution_data(doctype, name, filters)
    avg_contribution = total_contributions / total_members if total_members else 0
    
    return {
        "name": name,
        "type": doctype,
        "total_members": total_members,
        "total_contributions": total_contributions,
        "avg_contribution_per_member": avg_contribution,
        "last_contribution_date": last_contribution_date
    }

def get_parishes(filters):
    parish_filters = {}
    if filters.get("diocese"):
        parish_filters["diocese"] = filters.get("diocese")
    if filters.get("archdeaconry"):
        parish_filters["archdeaconry"] = filters.get("archdeaconry")
    if filters.get("parish"):
        parish_filters["name"] = filters.get("parish")
    return frappe.get_all("Parish", filters=parish_filters, fields=["name"])

def get_sub_parishes(parish):
    return frappe.get_all("Sub Parish", filters={"parish": parish}, fields=["name"])

def get_total_members(doctype, name):
    if doctype == "Parish":
        return frappe.db.count("Church Member", filters={"parish": name})
    elif doctype == "Sub Parish":
        return frappe.db.count("Church Member", filters={"sub_parish": name})
    return 0

def get_contribution_data(doctype, name, filters):
    date_filter = []
    if filters.get("from_date"):
        date_filter.append(["payment_date", ">=", filters.get("from_date")])
    if filters.get("to_date"):
        date_filter.append(["payment_date", "<=", filters.get("to_date")])

    if doctype == "Parish":
        members = frappe.get_all("Church Member", filters={"parish": name}, pluck="name")
    elif doctype == "Sub Parish":
        members = frappe.get_all("Church Member", filters={"sub_parish": name}, pluck="name")
    else:
        return 0, None

    if not members:
        return 0, None

    result = frappe.db.sql("""
        SELECT SUM(amount) as total, MAX(payment_date) as last_date
        FROM `tabChurch Payment`
        WHERE member IN (%s) AND docstatus = 1
        %s
    """ % (', '.join(['%s'] * len(members)), 
           "AND " + " AND ".join([f"{f[0]} {f[1]} %s" for f in date_filter]) if date_filter else ""),
    tuple(members + [f[2] for f in date_filter]), as_dict=True)

    total = result[0].total if result and result[0].total else 0
    last_date = result[0].last_date if result and result[0].last_date else None

    return total, last_date

def get_chart_data(data):
    labels = [d['name'] for d in data if d['type'] == 'Parish']
    contributions = [d['total_contributions'] for d in data if d['type'] == 'Parish']
    members = [d['total_members'] for d in data if d['type'] == 'Parish']

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Total Contributions",
                    "values": contributions
                },
                {
                    "name": "Total Members",
                    "values": members
                }
            ]
        },
        "type": "bar",
        "colors": ["#4CAF50", "#2196F3"]
    }

def get_summary(data):
    parish_data = [d for d in data if d['type'] == 'Parish']
    total_members = sum(d['total_members'] for d in parish_data)
    total_contributions = sum(d['total_contributions'] for d in parish_data)
    avg_contribution = total_contributions / total_members if total_members else 0
    last_contribution_date = max([d['last_contribution_date'] for d in parish_data if d['last_contribution_date']], default=None)

    return [
        {
            "value": total_members,
            "label": _("Total Members"),
            "datatype": "Int",
            "currency": None
        },
        {
            "value": total_contributions,
            "label": _("Total Contributions"),
            "datatype": "Currency",
            "currency": frappe.defaults.get_global_default("currency")
        },
        {
            "value": avg_contribution,
            "label": _("Average Contribution per Member"),
            "datatype": "Currency",
            "currency": frappe.defaults.get_global_default("currency")
        },
        {
            "value": last_contribution_date,
            "label": _("Last Contribution Date"),
            "datatype": "Date",
            "currency": None
        }
    ]