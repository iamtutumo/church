frappe.ui.form.on('Sub Parish', {
    refresh: function(frm) {
        // Custom button to view church members
        frm.add_custom_button(__('View Members'), function() {
            frappe.set_route('List', 'Church Member', {'sub_parish': frm.doc.name});
        });
    },
    validate: function(frm) {
        // Custom validation logic if needed
    }
});