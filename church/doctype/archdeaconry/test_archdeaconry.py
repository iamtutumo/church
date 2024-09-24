import frappe
import unittest

class TestArchdeaconry(unittest.TestCase):
    def setUp(self):
        # Setup test data
        self.diocese = frappe.get_doc({
            "doctype": "Diocese",
            "name1": "Test Diocese",
            "region": "Test Region"
        }).insert()

    def tearDown(self):
        # Clean up test data
        frappe.delete_doc("Diocese", self.diocese.name)

    def test_archdeaconry_creation(self):
        archdeaconry = frappe.get_doc({
            "doctype": "Archdeaconry",
            "name1": "Test Archdeaconry",
            "region": "Test Region",
            "diocese": self.diocese.name,
            "gps_coordinates": "0.0,0.0"
        }).insert()
        self.assertTrue(frappe.db.exists("Archdeaconry", archdeaconry.name))

    def test_invalid_gps_coordinates(self):
        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc({
                "doctype": "Archdeaconry",
                "name1": "Invalid Archdeaconry",
                "region": "Test Region",
                "diocese": self.diocese.name,
                "gps_coordinates": "invalid"
            }).insert()