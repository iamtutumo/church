frappe.ui.form.on('Archdeaconry', {
    refresh: function(frm) {
        // Custom button to view parishes
        frm.add_custom_button(__('View Parishes'), function() {
            frappe.set_route('List', 'Parish', {'archdeaconry': frm.doc.name});
        });
    },
    validate: function(frm) {
        // Custom validation logic if needed
    }
});