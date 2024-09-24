frappe.ui.form.on('Church Dependent', {
    refresh: function(frm) {
        // Custom button to view parent member
        if (frm.doc.parent_member) {
            frm.add_custom_button(__('View Parent Member'), function() {
                frappe.set_route('Form', 'Church Member', frm.doc.parent_member);
            });
        }
    },
    validate: function(frm) {
        // Custom validation logic if needed
    }
});