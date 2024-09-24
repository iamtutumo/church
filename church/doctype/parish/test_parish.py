import frappe
import unittest

class TestParish(unittest.TestCase):
    def setUp(self):
        # Setup test data
        self.diocese = frappe.get_doc({
            "doctype": "Diocese",
            "name1": "Test Diocese",
            "region": "Test Region"
        }).insert()
        self.archdeaconry = frappe.get_doc({
            "doctype": "Archdeaconry",
            "name1": "Test Archdeaconry",
            "region": "Test Region",
            "diocese": self.diocese.name
        }).insert()

    def tearDown(self):
        # Clean up test data
        frappe.delete_doc("Archdeaconry", self.archdeaconry.name)
        frappe.delete_doc("Diocese", self.diocese.name)

    def test_parish_creation(self):
        parish = frappe.get_doc({
            "doctype": "Parish",
            "name1": "Test Parish",
            "region": "Test Region",
            "archdeaconry": self.archdeaconry.name,
            "gps_coordinates": "0.0,0.0"
        }).insert()
        self.assertTrue(frappe.db.exists("Parish", parish.name))

    def test_invalid_gps_coordinates(self):
        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc({
                "doctype": "Parish",
                "name1": "Invalid Parish",
                "region": "Test Region",
                "archdeaconry": self.archdeaconry.name,
                "gps_coordinates": "invalid"
            }).insert()

    def test_archdeaconry_stats_update(self):
        initial_count = self.archdeaconry.total_parishes or 0
        parish = frappe.get_doc({
            "doctype": "Parish",
            "name1": "Test Parish",
            "region": "Test Region",
            "archdeaconry": self.archdeaconry.name
        }).insert()
        self.archdeaconry.reload()
        self.assertEqual(self.archdeaconry.total_parishes, initial_count + 1)