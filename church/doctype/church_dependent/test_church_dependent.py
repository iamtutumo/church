import frappe
import unittest
from datetime import datetime, timedelta

class TestChurchDependent(unittest.TestCase):
    def setUp(self):
        # Setup test data
        self.parent_member = frappe.get_doc({
            "doctype": "Church Member",
            "first_name": "Parent",
            "last_name": "Member",
            "date_of_birth": datetime.now() - timedelta(days=365*30)  # 30 years old
        }).insert()

    def tearDown(self):
        # Clean up test data
        frappe.delete_doc("Church Member", self.parent_member.name)

    def test_church_dependent_creation(self):
        dependent = frappe.get_doc({
            "doctype": "Church Dependent",
            "first_name": "Child",
            "last_name": "Dependent",
            "date_of_birth": datetime.now() - timedelta(days=365*10),  # 10 years old
            "relationship": "Child",
            "parent_member": self.parent_member.name
        }).insert()
        self.assertTrue(frappe.db.exists("Church Dependent", dependent.name))

    def test_invalid_date_of_birth(self):
        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc({
                "doctype": "Church Dependent",
                "first_name": "Future",
                "last_name": "Child",
                "date_of_birth": datetime.now() + timedelta(days=365),  # 1 year in the future
                "relationship": "Child",
                "parent_member": self.parent_member.name
            }).insert()

    def test_adult_child_warning(self):
        with self.assertRaises(frappe.MandatoryError):
            dependent = frappe.get_doc({
                "doctype": "Church Dependent",
                "first_name": "Adult",
                "last_name": "Child",
                "date_of_birth": datetime.now() - timedelta(days=365*20),  # 20 years old
                "relationship": "Child",
                "parent_member": self.parent_member.name
            }).insert()
            # Check if a message was thrown (you might need to adjust this based on how you implement the warning)
            self.assertTrue(any("Note: This dependent is 18 years or older" in msg for msg in frappe.message_log))

    def test_dependent_older_than_parent(self):
        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc({
                "doctype": "Church Dependent",
                "first_name": "Older",
                "last_name": "Dependent",
                "date_of_birth": datetime.now() - timedelta(days=365*40),  # 40 years old
                "relationship": "Sibling",
                "parent_member": self.parent_member.name
            }).insert()