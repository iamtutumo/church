import frappe
import requests
from geopy.distance import geodesic

def get_coordinates(address):
    """
    Get latitude and longitude for a given address using a geocoding service.
    """
    api_key = frappe.get_single("Church Settings").get_password("geocoding_api_key")
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    params = {
        "address": address,
        "key": api_key
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        frappe.log_error(f"Geocoding failed for address: {address}", "GPS Error")
        return None, None

def calculate_distance(coord1, coord2):
    """
    Calculate the distance between two coordinates in kilometers.
    """
    return geodesic(coord1, coord2).kilometers

def update_entity_coordinates(doctype, name):
    """
    Update the coordinates for a given entity (Parish, Archdeaconry, Diocese).
    """
    doc = frappe.get_doc(doctype, name)
    address = f"{doc.address_line1}, {doc.city}, {doc.country}"
    lat, lng = get_coordinates(address)
    
    if lat and lng:
        doc.latitude = lat
        doc.longitude = lng
        doc.save()
        frappe.db.commit()
        frappe.msgprint(f"Coordinates updated for {doctype} {name}")
    else:
        frappe.msgprint(f"Failed to update coordinates for {doctype} {name}")