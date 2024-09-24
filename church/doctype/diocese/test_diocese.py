import frappe
import unittest

class TestDiocese(unittest.TestCase):
    def setUp(self):
        # Setup test data
        pass

    def tearDown(self):
        # Clean up test data
        pass

    def test_diocese_creation(self):
        diocese = frappe.get_doc({
            "doctype": "Diocese",
            "name1": "Test Diocese",
            "region": "Test Region",
            "gps_coordinates": "0.0,0.0"
        }).insert()
        self.assertTrue(frappe.db.exists("Diocese", diocese.name))

    def test_invalid_gps_coordinates(self):
        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc({
                "doctype": "Diocese",
                "name1": "Invalid Diocese",
                "region": "Test Region",
                "gps_coordinates": "invalid"
            }).insert()