import frappe
from frappe import _
from frappe.model.document import Document

class ChurchMember(Document):
    def validate(self):
        self.set_full_name()
        self.validate_age()
        self.set_member_id()

    def set_full_name(self):
        self.full_name = f"{self.first_name} {self.last_name}"

    def validate_age(self):
        if self.date_of_birth:
            age = frappe.utils.date_diff(frappe.utils.nowdate(), self.date_of_birth) / 365
            if age < 0:
                frappe.throw(_("Date of Birth cannot be in the future."))

    def set_member_id(self):
        if not self.member_id:
            # Generate a unique member ID
            last_id = frappe.db.sql("""
                SELECT member_id FROM `tabChurch Member`
                WHERE parish = %s
                ORDER BY creation DESC LIMIT 1
            """, self.parish)
            
            if last_id:
                last_num = int(last_id[0][0].split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1

            self.member_id = f"{self.parish}-{new_num:04d}"

    def on_update(self):
        self.update_member_count()

    def on_trash(self):
        self.update_member_count()

    def update_member_count(self):
        for doctype in ['Parish', 'Archdeaconry', 'Diocese']:
            if hasattr(self, doctype.lower()):
                count = frappe.db.count('Church Member', {doctype.lower(): getattr(self, doctype.lower())})
                frappe.db.set_value(doctype, getattr(self, doctype.lower()), 'total_members', count)