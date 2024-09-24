import frappe
import unittest

class TestChurchPayment(unittest.TestCase):
    def setUp(self):
        # Setup test data
        self.member = frappe.get_doc({
            "doctype": "Church Member",
            "first_name": "Test",
            "last_name": "Member"
        }).insert()

    def tearDown(self):
        # Clean up test data
        frappe.delete_doc("Church Member", self.member.name)

    def test_church_payment_creation(self):
        payment = frappe.get_doc({
            "doctype": "Church Payment",
            "member": self.member.name,
            "amount": 1000,
            "payment_date": frappe.utils.nowdate(),
            "payment_method": "Cash"
        }).insert()
        self.assertTrue(frappe.db.exists("Church Payment", payment.name))

    def test_invalid_amount(self):
        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc({
                "doctype": "Church Payment",
                "member": self.member.name,
                "amount": 0,
                "payment_date": frappe.utils.nowdate(),
                "payment_method": "Cash"
            }).insert()

    def test_member_contribution_update(self):
        initial_contribution = self.member.total_contributions or 0
        payment = frappe.get_doc({
            "doctype": "Church Payment",
            "member": self.member.name,
            "amount": 1000,
            "payment_date": frappe.utils.nowdate(),
            "payment_method": "Cash"
        }).insert()
        payment.submit()

        self.member.reload()
        self.assertEqual(self.member.total_contributions, initial_contribution + 1000)

        payment.cancel()
        self.member.reload()
        self.assertEqual(self.member.total_contributions, initial_contribution)