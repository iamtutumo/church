import frappe
from frappe.model.document import Document

class ChurchPayment(Document):
    def validate(self):
        self.validate_amount()

    def validate_amount(self):
        if self.amount <= 0:
            frappe.throw("Payment amount must be greater than zero")

    def on_submit(self):
        self.update_member_contributions()

    def on_cancel(self):
        self.update_member_contributions()

    def update_member_contributions(self):
        member = frappe.get_doc("Church Member", self.member)
        member.update_total_contributions()

    def before_insert(self):
        self.set_missing_values()

    def set_missing_values(self):
        if not self.payment_date:
            self.payment_date = frappe.utils.nowdate()