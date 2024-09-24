import frappe
import requests
from frappe import _

def process_payment(payment_doc):
    """
    Process a payment using a payment gateway.
    """
    settings = frappe.get_single("Church Settings")
    gateway_url = settings.payment_gateway_url
    api_key = settings.get_password("payment_gateway_api_key")

    payload = {
        "amount": payment_doc.amount,
        "currency": payment_doc.currency,
        "source": payment_doc.payment_method,
        "description": f"Payment for {payment_doc.contribution_type}",
        "customer": {
            "email": payment_doc.email,
            "name": payment_doc.member_name
        }
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(gateway_url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        if result.get("status") == "succeeded":
            payment_doc.payment_id = result.get("id")
            payment_doc.status = "Paid"
            payment_doc.save()
            frappe.db.commit()
            frappe.msgprint(_("Payment processed successfully"))
        else:
            frappe.throw(_("Payment processing failed"))

    except requests.exceptions.RequestException as e:
        frappe.log_error(f"Payment gateway error: {str(e)}", "Payment Processing Error")
        frappe.throw(_("An error occurred while processing the payment"))

def refund_payment(payment_doc):
    """
    Refund a processed payment.
    """
    settings = frappe.get_single("Church Settings")
    refund_url = f"{settings.payment_gateway_url}/refunds"
    api_key = settings.get_password("payment_gateway_api_key")

    payload = {
        "payment_intent": payment_doc.payment_id,
        "amount": payment_doc.amount
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(refund_url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        if result.get("status") == "succeeded":
            payment_doc.status = "Refunded"
            payment_doc.save()
            frappe.db.commit()
            frappe.msgprint(_("Payment refunded successfully"))
        else:
            frappe.throw(_("Payment refund failed"))

    except requests.exceptions.RequestException as e:
        frappe.log_error(f"Payment gateway error: {str(e)}", "Refund Processing Error")
        frappe.throw(_("An error occurred while processing the refund"))