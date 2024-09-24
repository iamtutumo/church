from . import __version__ as app_version

app_name = "church"
app_title = "Church Management"
app_publisher = "Upsyd Limited"
app_description = "A comprehensive church management system"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "etu.moses@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/church/css/church.css"
app_include_js = "/assets/church/js/church.js"

# include js, css files in header of web template
web_include_css = "/assets/church/css/church.css"
web_include_js = "/assets/church/js/church.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "church/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Church Member" : "public/js/church_member.js",
    "Church Payment" : "public/js/church_payment.js",
    "Church Event" : "public/js/church_event.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#   "Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "church.install.before_install"
# after_install = "church.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "church.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#   "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#   "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#   "ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Church Member": {
        "after_insert": "church.church.doctype.church_member.church_member.after_member_insert",
        "on_update": "church.church.doctype.church_member.church_member.on_member_update",
    },
    "Church Payment": {
        "on_submit": "church.church.doctype.church_payment.church_payment.on_payment_submit",
        "on_cancel": "church.church.doctype.church_payment.church_payment.on_payment_cancel",
    },
    "Church Event": {
        "after_insert": "church.church.doctype.church_event.church_event.after_event_insert",
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
        "church.tasks.daily"
    ],
    "weekly": [
        "church.tasks.weekly"
    ],
    "monthly": [
        "church.tasks.monthly"
    ]
}

# Testing
# -------

# before_tests = "church.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#   "frappe.desk.doctype.event.event.get_events": "church.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#   "Task": "church.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {
        "doctype": "{doctype_4}"
    }
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#   "church.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []