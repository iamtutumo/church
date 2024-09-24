frappe.query_reports["Contribution Summary"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -12),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "diocese",
            "label": __("Diocese"),
            "fieldtype": "Link",
            "options": "Diocese"
        },
        {
            "fieldname": "archdeaconry",
            "label": __("Archdeaconry"),
            "fieldtype": "Link",
            "options": "Archdeaconry",
            "get_query": function() {
                var diocese = frappe.query_report.get_filter_value('diocese');
                if (diocese) {
                    return {
                        filters: {
                            'diocese': diocese
                        }
                    };
                }
            }
        },
        {
            "fieldname": "parish",
            "label": __("Parish"),
            "fieldtype": "Link",
            "options": "Parish",
            "get_query": function() {
                var archdeaconry = frappe.query_report.get_filter_value('archdeaconry');
                if (archdeaconry) {
                    return {
                        filters: {
                            'archdeaconry': archdeaconry
                        }
                    };
                }
            }
        },
        {
            "fieldname": "contribution_type",
            "label": __("Contribution Type"),
            "fieldtype": "Link",
            "options": "Contribution Type"
        },
        {
            "fieldname": "group_by",
            "label": __("Group By"),
            "fieldtype": "Select",
            "options": "Month\nQuarter\nYear\nContribution Type",
            "default": "Month"
        }
    ],
    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname == "total_amount" && data && data.total_amount > 0) {
            value = "<span style='color:green'>" + value + "</span>";
        }
        return value;
    },
    "onload": function(report) {
        report.page.add_inner_button(__("Export Details"), function() {
            var filters = report.get_values();
            frappe.set_route('query-report', 'Contribution Details', {filters: filters});
        });
    },
    "get_chart_data": function(columns, result) {
        return {
            data: {
                labels: result.map(function(d) { return d.group_by; }),
                datasets: [{
                    name: "Total Contributions",
                    values: result.map(function(d) { return d.total_amount; })
                }]
            },
            type: 'line',
            colors: ['#4CAF50']
        }
    },
    "get_chart_options": function(columns, result) {
        return {
            title: {
                text: 'Contribution Trend'
            },
            subtitle: {
                text: 'Total Contributions Over Time'
            },
            xAxis: {
                title: {
                    text: frappe.query_report.get_filter_value('group_by')
                }
            },
            yAxis: {
                title: {
                    text: 'Total Contributions'
                }
            }
        }
    }
};