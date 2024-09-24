frappe.ui.form.on('Church Member', {
    refresh: function(frm) {
        // Custom button to view payments
        frm.add_custom_button(__('View Payments'), function() {
            frappe.set_route('List', 'Church Payment', {'member': frm.doc.name});
        });

        // Custom button to add dependent
        frm.add_custom_button(__('Add Dependent'), function() {
            frappe.new_doc('Church Dependent', {
                'parent_member': frm.doc.name
            });
        });
    },
    validate: function(frm) {
        // Custom validation logic if needed
    }
});