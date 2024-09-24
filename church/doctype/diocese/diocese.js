frappe.ui.form.on('Diocese', {
    refresh: function(frm) {
        // Custom button to view archdeaconries
        frm.add_custom_button(__('View Archdeaconries'), function() {
            frappe.set_route('List', 'Archdeaconry', {'diocese': frm.doc.name});
        });
    },
    validate: function(frm) {
        // Custom validation logic if needed
    }
});