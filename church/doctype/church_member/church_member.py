import frappe
from frappe.model.document import Document
import uuid

class ChurchMember(Document):
    def validate(self):
        self.generate_unique_payment_id()

    def generate_unique_payment_id(self):
        if not self.unique_payment_id:
            self.unique_payment_id = str(uuid.uuid4())[:8].upper()

    def on_update(self):
        self.update_total_contributions()

    def update_total_contributions(self):
        total = frappe.db.sql("""
            SELECT SUM(amount) FROM `tabChurch Payment`
            WHERE member = %s AND docstatus = 1
        """, self.name)
        self.total_contributions = total[0][0] if total and total[0][0] else 0
        self.db_update()

    def get_dependents(self):
        return frappe.get_all('Church Dependent', filters={'parent_member': self.name})