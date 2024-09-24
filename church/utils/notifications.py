import frappe
from frappe.utils import get_url_to_form

def send_email_notification(recipient, subject, message, reference_doctype=None, reference_name=None):
    """
    Send an email notification to a recipient.
    """
    try:
        frappe.sendmail(
            recipients=[recipient],
            subject=subject,
            message=message,
            reference_doctype=reference_doctype,
            reference_name=reference_name
        )
        frappe.msgprint(f"Email notification sent to {recipient}")
    except Exception as e:
        frappe.log_error(f"Failed to send email notification: {str(e)}", "Email Notification Error")

def send_sms_notification(phone_number, message):
    """
    Send an SMS notification to a phone number.
    """
    try:
        from frappe.core.doctype.sms_settings.sms_settings import send_sms
        send_sms([phone_number], message)
        frappe.msgprint(f"SMS notification sent to {phone_number}")
    except Exception as e:
        frappe.log_error(f"Failed to send SMS notification: {str(e)}", "SMS Notification Error")

def notify_upcoming_event(event):
    """
    Send notifications for an upcoming church event.
    """
    subject = f"Upcoming Event: {event.event_name}"
    message = f"""
    Dear Member,

    We have an upcoming event:

    Event: {event.event_name}
    Date: {event.event_date}
    Time: {event.event_time}
    Venue: {event.venue}

    We look forward to your participation!

    Best regards,
    Church Management Team
    """
    
    for participant in event.participants:
        if participant.email:
            send_email_notification(participant.email, subject, message, "Church Event", event.name)
        if participant.phone:
            sms_message = f"Reminder: {event.event_name} on {event.event_date} at {event.event_time}, {event.venue}"
            send_sms_notification(participant.phone, sms_message)