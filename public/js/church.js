frappe.provide('church');

church = {
    setup_quick_entry: function() {
        // Override quick entry for Church Member
        frappe.ui.form.make_quick_entry = (function() {
            var original = frappe.ui.form.make_quick_entry;
            return function(doctype, after_insert) {
                if (doctype === 'Church Member') {
                    frappe.quick_entry = new church.ChurchMemberQuickEntry({ doctype: doctype, after_insert: after_insert });
                    return frappe.quick_entry.setup();
                }
                return original(doctype, after_insert);
            };
        })();
    },

    ChurchMemberQuickEntry: class ChurchMemberQuickEntry extends frappe.ui.form.QuickEntryForm {
        constructor(opts) {
            super(opts);
        }

        render_dialog() {
            this.mandatory = [
                {fieldtype: "Data", label: "First Name", fieldname: "first_name", reqd: 1},
                {fieldtype: "Data", label: "Last Name", fieldname: "last_name", reqd: 1},
                {fieldtype: "Date", label: "Date of Birth", fieldname: "date_of_birth", reqd: 1},
                {fieldtype: "Link", label: "Parish", fieldname: "parish", options: "Parish", reqd: 1},
                {fieldtype: "Data", label: "Email", fieldname: "email"},
                {fieldtype: "Data", label: "Phone", fieldname: "phone"}
            ];
            super.render_dialog();
        }
    },

    setup_church_dashboard: function(frm) {
        if(frm.doc.__islocal)
            return;
        
        frm.dashboard.add_indicator(__("Total Members: {0}", [frm.doc.total_members || 0]), "blue");
        frm.dashboard.add_indicator(__("Total Contributions: {0}", [format_currency(frm.doc.total_contributions || 0, frm.doc.default_currency)]), "green");
    },

    setup_member_quick_view: function() {
        $('body').on('click', '.church-member-link', function() {
            var member_name = $(this).data('member');
            frappe.quick_view('Church Member', member_name);
        });
    },

    format_currency: function(value, currency) {
        if (currency) return format_currency(value, currency);
        return format_currency(value);
    },

    setup_contribution_graph: function(frm) {
        frappe.call({
            method: "church.utils.get_contribution_data",
            args: {
                doctype: frm.doctype,
                name: frm.docname
            },
            callback: function(r) {
                if (r.message) {
                    let data = r.message;
                    frm.dashboard.add_chart({
                        title: "Monthly Contributions",
                        data: {
                            labels: data.labels,
                            datasets: [
                                {
                                    name: "Contributions",
                                    values: data.values
                                }
                            ]
                        },
                        type: 'bar',
                        height: 250
                    });
                }
            }
        });
    }
};

$(document).ready(function() {
    church.setup_quick_entry();
    church.setup_member_quick_view();
});