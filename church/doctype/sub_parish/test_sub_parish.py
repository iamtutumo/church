import frappe
import unittest

class TestSubParish(unittest.TestCase):
    def setUp(self):
        # Setup test data
        self.diocese = frappe.get_doc({"doctype": "Diocese", "name1": "Test Diocese", "region": "Test Region"}).insert()
        self.archdeaconry = frappe.get_doc({
            "doctype": "Archdeaconry",
            "name1": "Test Archdeaconry",
            "region": "Test Region",
            "diocese": self.diocese.name
        }).insert()
        self.parish = frappe.get_doc({
            "doctype": "Parish",
            "name1": "Test Parish",
            "region": "Test Region",
            "archdeaconry": self.archdeaconry.name
        }).insert()

    def tearDown(self):
        # Clean up test data
        frappe.delete_doc("Parish", self.parish.name)
        frappe.delete_doc("Archdeaconry", self.archdeaconry.name)
        frappe.delete_doc("Diocese", self.diocese.name)

    def test_sub_parish_creation(self):
        sub_parish = frappe.get_doc({
            "doctype": "Sub Parish",
            "name1": "Test Sub Parish",
            "region": "Test Region",
            "parish": self.parish.name,
            "gps_coordinates": "0.0,0.0"
        }).insert()
        self.assertTrue(frappe.db.exists("Sub Parish", sub_parish.name))

    def test_invalid_gps_coordinates(self):
        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc({
                "doctype": "Sub Parish",
                "name1": "Invalid Sub Parish",
                "region": "Test Region",
                "parish": self.parish.name,
                "gps_coordinates": "invalid"
            }).insert()

    def test_parish_stats_update(self):
        initial_count = self.parish.total_sub_parishes or 0
        sub_parish = frappe.get_doc({
            "doctype": "Sub Parish",
            "name1": "Test Sub Parish",
            "region": "Test Region",
            "parish": self.parish.name
        }).insert()
        self.parish.reload()
        self.assertEqual(self.parish.total_sub_parishes, initial_count + 1)