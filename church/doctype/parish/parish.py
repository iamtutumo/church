import frappe
from frappe.model.document import Document

class Parish(Document):
    def validate(self):
        self.validate_coordinates()

    def validate_coordinates(self):
        if self.gps_coordinates:
            coords = self.gps_coordinates.split(',')
            if len(coords) != 2:
                frappe.throw("GPS Coordinates should be in the format 'latitude,longitude'")
            try:
                lat, lon = float(coords[0]), float(coords[1])
                if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    frappe.throw("Invalid GPS Coordinates")
            except ValueError:
                frappe.throw("GPS Coordinates should be numeric values")

    def on_update(self):
        self.update_archdeaconry_stats()

    def update_archdeaconry_stats(self):
        # Update statistics in the parent Archdeaconry
        archdeaconry = frappe.get_doc("Archdeaconry", self.archdeaconry)
        archdeaconry.total_parishes = frappe.db.count("Parish", {"archdeaconry": self.archdeaconry})
        archdeaconry.save()