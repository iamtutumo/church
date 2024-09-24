frappe.query_reports["Parish Dashboard"] = {
    "filters": [
        {
            "fieldname": "diocese",
            "label": __("Diocese"),
            "fieldtype": "Link",
            "options": "Diocese",
            "get_query": function() {
                return {
                    filters: {
                        "is_group": 1
                    }
                };
            }
        },
        {
            "fieldname": "archdeaconry",
            "label": __("Archdeaconry"),
            "fieldtype": "Link",
            "options": "Archdeaconry",
            "get_query": function() {
                var diocese = frappe.query_report.get_filter_value('diocese');
                return {
                    filters: {
                        "diocese": diocese
                    }
                };
            },
            "depends_on": "diocese"
        },
        {
            "fieldname": "parish",
            "label": __("Parish"),
            "fieldtype": "Link",
            "options": "Parish",
            "get_query": function() {
                var archdeaconry = frappe.query_report.get_filter_value('archdeaconry');
                return {
                    filters: {
                        "archdeaconry": archdeaconry
                    }
                };
            },
            "depends_on": "archdeaconry"
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        }
    ],
    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname == "total_contributions" && data && data.total_contributions) {
            value = "<span style='color:green'>" + value + "</span>";
        }
        if (column.fieldname == "avg_contribution_per_member" && data && data.avg_contribution_per_member) {
            value = "<span style='color:blue'>" + value + "</span>";
        }
        return value;
    },
    "tree": true,
    "name_field": "name",
    "parent_field": "parent",
    "initial_depth": 1,
    "onload": function(report) {
        report.page.add_inner_button(__("View on Map"), function() {
            frappe.set_route("gps-dashboard", {"entity_type": "Parish"});
        });
    },
    "get_datatable_options": function(options) {
        return Object.assign(options, {
            treeView: true,
            cellHeight: 45,
            columns: [
                { name: "name", width: 300 },
                { name: "type", width: 100 },
                { name: "total_members", width: 120 },
                { name: "total_contributions", width: 150 },
                { name: "avg_contribution_per_member", width: 180 },
                { name: "last_contribution_date", width: 150 }
            ]
        });
    },
    "get_chart_data": function(columns, result) {
        return {
            data: {
                labels: result.filter(d => d.type === "Parish").map(d => d.name),
                datasets: [
                    {
                        name: "Total Members",
                        values: result.filter(d => d.type === "Parish").map(d => d.total_members)
                    },
                    {
                        name: "Total Contributions",
                        values: result.filter(d => d.type === "Parish").map(d => d.total_contributions)
                    }
                ]
            },
            type: 'bar',
            colors: ['#7cd6fd', '#743ee2']
        }
    },
    "after_datatable_render": function(datatable_obj) {
        $(datatable_obj.wrapper).find(".dt-row-0").find('input[type=checkbox]').click();
    },
    "get_chart_options": function(columns, result) {
        return {
            title: {
                text: 'Parish Overview'
            },
            subtitle: {
                text: 'Members and Contributions'
            },
            xAxis: {
                title: {
                    text: 'Parish'
                }
            },
            yAxis: [
                {
                    title: {
                        text: 'Total Members'
                    }
                },
                {
                    title: {
                        text: 'Total Contributions'
                    },
                    opposite: true
                }
            ]
        }
    }
};