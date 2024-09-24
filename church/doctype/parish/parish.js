frappe.ui.form.on('Parish', {
    refresh: function(frm) {
        // Custom button to view sub-parishes
        frm.add_custom_button(__('View Sub-Parishes'), function() {
            frappe.set_route('List', 'Sub Parish', {'parish': frm.doc.name});
        });

        // Custom button to view church members
        frm.add_custom_button(__('View Members'), function() {
            frappe.set_route('List', 'Church Member', {'parish': frm.doc.name});
        });
    },
    validate: function(frm) {
        // Custom validation logic if needed
    }
});