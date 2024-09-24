import frappe
from frappe.model.document import Document

class ChurchDependent(Document):
    def validate(self):
        self.validate_age()
        self.validate_parent_member()

    def validate_age(self):
        if self.date_of_birth:
            age = frappe.utils.date_diff(frappe.utils.nowdate(), self.date_of_birth) / 365
            if age < 0:
                frappe.throw("Date of Birth cannot be in the future")
            if self.relationship == "Child" and age >= 18:
                frappe.msgprint("Note: This dependent is 18 years or older")

    def validate_parent_member(self):
        if self.parent_member:
            parent = frappe.get_doc("Church Member", self.parent_member)
            if parent.date_of_birth and self.date_of_birth:
                if self.date_of_birth < parent.date_of_birth:
                    frappe.throw("Dependent's date of birth cannot be earlier than the parent member's date of birth")

    def on_update(self):
        self.update_parent_member()

    def update_parent_member(self):
        parent = frappe.get_doc("Church Member", self.parent_member)
        parent.save()  # This will trigger any necessary updates on the parent member