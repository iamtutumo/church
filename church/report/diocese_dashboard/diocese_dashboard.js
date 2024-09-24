frappe.query_reports["Diocese Dashboard"] = {
    "filters": [
        {
            "fieldname": "diocese",
            "label": __("Diocese"),
            "fieldtype": "Link",
            "options": "Diocese"
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        }
    ],
    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname == "total_contributions" && data && data.total_contributions) {
            value = "<span style='color:green'>" + value + "</span>";
        }
        return value;
    },
    "onload": function(report) {
        report.page.add_inner_button(__("View on Map"), function() {
            frappe.set_route("gps-dashboard");
        });
    },
    "tree": true,
    "name_field": "name",
    "parent_field": "parent",
    "initial_depth": 1
};

diocese_dashboard.js
church/church/report/diocese_dashboard/diocese_dashboard.py:
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "name",
            "label": _("Name"),

diocese_dashboard.py
Avatar for etu.moses-kdevf
Tutu Moses



