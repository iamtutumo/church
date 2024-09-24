import frappe
from frappe import _
from frappe.model.document import Document

class ChurchPayment(Document):
    def validate(self):
        self.validate_amount()
        self.set_member_details()

    def validate_amount(self):
        if self.amount <= 0:
            frappe.throw(_("Payment amount must be greater than zero."))

    def set_member_details(self):
        if self.member:
            member = frappe.get_doc("Church Member", self.member)
            self.member_name = member.full_name
            self.parish = member.parish
            self.archdeaconry = member.archdeaconry
            self.diocese = member.diocese

    def on_submit(self):
        self.update_member_last_contribution()

    def on_cancel(self):
        self.update_member_last_contribution()

    def update_member_last_contribution(self):
        if self.member:
            last_contribution = frappe.get_all(
                "Church Payment",
                filters={
                    "member": self.member,
                    "docstatus": 1,
                    "name": ("!=", self.name)
                },
                order_by="payment_date desc",
                limit=1,
                pluck="payment_date"
            )

            frappe.db.set_value("Church Member", self.member, 
                                "last_contribution_date", 
                                last_contribution[0] if last_contribution else None)