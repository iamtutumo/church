frappe.ui.form.on('Church Payment', {
    refresh: function(frm) {
        if(frm.doc.docstatus === 1) {
            frm.add_custom_button(__('View Member'), function() {
                frappe.set_route('Form', 'Church Member', frm.doc.member);
            });
        }
    },
    validate: function(frm) {
        // Custom validation logic if needed
    }
});