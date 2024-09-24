import frappe

@frappe.whitelist()
def get_gps_data(entity_type='all'):
    entities = []
    doctypes = ['Diocese', 'Archdeaconry', 'Parish', 'Sub Parish']
    
    if entity_type != 'all':
        doctypes = [entity_type]

    for doctype in doctypes:
        docs = frappe.get_all(doctype, 
                              fields=['name', 'gps_coordinates'],
                              filters={'gps_coordinates': ('!=', '')})
        
        for doc in docs:
            if doc.gps_coordinates:
                lat, lon = map(float, doc.gps_coordinates.split(','))
                total_contributions = get_total_contributions(doctype, doc.name)
                entities.append({
                    'name': doc.name,
                    'entity_type': doctype,
                    'latitude': lat,
                    'longitude': lon,
                    'total_contributions': total_contributions
                })
    
    return entities

def get_total_contributions(doctype, name):
    # This function should be implemented to calculate total contributions
    # for the given entity. The implementation will depend on your data structure.
    # Here's a placeholder implementation:
    return frappe.get_value(doctype, name, 'total_contributions') or 0