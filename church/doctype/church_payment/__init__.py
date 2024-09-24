import frappe
import unittest

class TestChurchMember(unittest.TestCase):
    def setUp(self):
        # Setup test data
        self.sub_parish = frappe.get_doc({
            "doctype": "Sub Parish",
            "name1": "Test Sub Parish",
            "region": "Test Region"
        }).insert()

    def tearDown(self):
        # Clean up test data
        frappe.delete_doc("Sub Parish", self.sub_parish.name)

    def test_church_member_creation(self):
        member = frappe.get_doc({
            "doctype": "Church Member",
            "first_name": "John",
            "last_name": "Doe",
            "sub_parish": self.sub_parish.name
        }).insert()
        self.assertTrue(frappe.db.exists("Church Member", member.name))
        self.assertTrue(member.unique_payment_id)

    def test_total_contributions_update(self):
        member = frappe.get_doc({
            "doctype": "Church Member",
            "first_name": "Jane",
            "last_name": "Doe",
            "sub_parish": self.sub_parish.name
        }).insert()

        # Create a payment
        payment = frappe.get_doc({
            "doctype": "Church Payment",
            "member": member.name,
            "amount": 1000,
            "payment_date": frappe.utils.nowdate()
        }).insert()
        payment.submit()

        member.reload()
        self.assertEqual(member.total_contributions, 1000)