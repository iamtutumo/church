import frappe
from frappe import _

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
        }
    ]

def get_data(filters):
    data = []
    dioceses = get_dioceses(filters)
    
    for diocese in dioceses:
        diocese_data = get_entity_data("Diocese", diocese.name, filters)
        diocese_data["parent"] = None
        data.append(diocese_data)
        
        archdeaconries = get_archdeaconries(diocese.name)
        for archdeaconry in archdeaconries:
            archdeaconry_data = get_entity_data("Archdeaconry", archdeaconry.name, filters)
            archdeaconry_data["parent"] = diocese.name
            data.append(archdeaconry_data)
            
            parishes = get_parishes(archdeaconry.name)
            for parish in parishes:
                parish_data = get_entity_data("Parish", parish.name, filters)
                parish_data["parent"] = archdeaconry.name
                data.append(parish_data)

    return data

def get_entity_data(doctype, name, filters):
    total_members = get_total_members(doctype, name)
    total_contributions = get_total_contributions(doctype, name, filters)
    avg_contribution = total_contributions / total_members if total_members else 0
    
    return {
        "name": name,
        "type": doctype,
        "total_members": total_members,
        "total_contributions": total_contributions,
        "avg_contribution_per_member": avg_contribution
    }

def get_dioceses(filters):
    diocese_filters = {}
    if filters.get("diocese"):
        diocese_filters["name"] = filters.get("diocese")
    return frappe.get_all("Diocese", filters=diocese_filters, fields=["name"])

def get_archdeaconries(diocese):
    return frappe.get_all("Archdeaconry", filters={"diocese": diocese}, fields=["name"])

def get_parishes(archdeaconry):
    return frappe.get_all("Parish", filters={"archdeaconry": archdeaconry}, fields=["name"])

def get_total_members(doctype, name):
    if doctype == "Diocese":
        return frappe.db.count("Church Member", filters={"diocese": name})
    elif doctype == "Archdeaconry":
        return frappe.db.count("Church Member", filters={"archdeaconry": name})
    elif doctype == "Parish":
        return frappe.db.count("Church Member", filters={"parish": name})
    return 0

def get_total_contributions(doctype, name, filters):
    date_filter = []
    if filters.get("from_date"):
        date_filter.append(["payment_date", ">=", filters.get("from_date")])
    if filters.get("to_date"):
        date_filter.append(["payment_date", "<=", filters.get("to_date")])

    if doctype == "Diocese":
        members = frappe.get_all("Church Member", filters={"diocese": name}, pluck="name")
    elif doctype == "Archdeaconry":
        members = frappe.get_all("Church Member", filters={"archdeaconry": name}, pluck="name")
    elif doctype == "Parish":
        members = frappe.get_all("Church Member", filters={"parish": name}, pluck="name")
    else:
        return 0

    if not members:
        return 0

    total = frappe.db.sql("""
        SELECT SUM(amount) 
        FROM `tabChurch Payment`
        WHERE member IN (%s) AND docstatus = 1
        %s
    """ % (', '.join(['%s'] * len(members)), 
           "AND " + " AND ".join([f"{f[0]} {f[1]} %s" for f in date_filter]) if date_filter else ""),
    tuple(members + [f[2] for f in date_filter]))

    return total[0][0] if total and total[0][0] else 0

def get_chart_data(data):
    labels = [d['name'] for d in data if d['type'] == 'Diocese']
    contributions = [d['total_contributions'] for d in data if d['type'] == 'Diocese']
    members = [d['total_members'] for d in data if d['type'] == 'Diocese']

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
    total_members = sum(d['total_members'] for d in data if d['type'] == 'Diocese')
    total_contributions = sum(d['total_contributions'] for d in data if d['type'] == 'Diocese')
    avg_contribution = total_contributions / total_members if total_members else 0

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
        }
    ]