from frappe import _

def get_data():
    return [
        {
            "label": _("Membership"),
            "icon": "fa fa-users",
            "items": [
                {
                    "type": "doctype",
                    "name": "Church Member",
                    "description": _("Manage church members"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Membership Application",
                    "description": _("Process new membership applications"),
                },
                {
                    "type": "report",
                    "name": "Member Directory",
                    "doctype": "Church Member",
                    "is_query_report": True,
                },
            ]
        },
        {
            "label": _("Contributions"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Church Payment",
                    "description": _("Record member contributions"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Contribution Type",
                    "description": _("Manage types of contributions"),
                },
                {
                    "type": "report",
                    "name": "Contribution Summary",
                    "doctype": "Church Payment",
                    "is_query_report": True,
                },
            ]
        },
        {
            "label": _("Church Structure"),
            "icon": "fa fa-sitemap",
            "items": [
                {
                    "type": "doctype",
                    "name": "Diocese",
                    "description": _("Manage dioceses"),
                },
                {
                    "type": "doctype",
                    "name": "Archdeaconry",
                    "description": _("Manage archdeaconries"),
                },
                {
                    "type": "doctype",
                    "name": "Parish",
                    "description": _("Manage parishes"),
                    "onboard": 1,
                },
            ]
        },
        {
            "label": _("Events"),
            "icon": "fa fa-calendar",
            "items": [
                {
                    "type": "doctype",
                    "name": "Church Event",
                    "description": _("Manage church events"),
                },
                {
                    "type": "doctype",
                    "name": "Event Registration",
                    "description": _("Manage event registrations"),
                },
            ]
        },
        {
            "label": _("Reports"),
            "icon": "fa fa-list",
            "items": [
                {
                    "type": "report",
                    "name": "Diocese Dashboard",
                    "doctype": "Diocese",
                    "is_query_report": True,
                },
                {
                    "type": "report",
                    "name": "Archdeaconry Dashboard",
                    "doctype": "Archdeaconry",
                    "is_query_report": True,
                },
                {
                    "type": "report",
                    "name": "Parish Dashboard",
                    "doctype": "Parish",
                    "is_query_report": True,
                },
                {
                    "type": "report",
                    "name": "Contribution Details",
                    "doctype": "Church Payment",
                    "is_query_report": True,
                },
            ]
        },
        {
            "label": _("Settings"),
            "icon": "fa fa-cog",
            "items": [
                {
                    "type": "doctype",
                    "name": "Church Settings",
                    "description": _("Configure church app settings"),
                },
            ]
        },
    ]

