from . import __version__ as app_version

app_name = "novacept_email_post"
app_title = "Novacept Email Post"
app_publisher = "Novacept Limited"
app_description = "Email posting for novacept"
app_email = "info@novacept.io"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/novacept_email_post/css/novacept_email_post.css"
# app_include_js = "/assets/novacept_email_post/js/novacept_email_post.js"

# include js, css files in header of web template
# web_include_css = "/assets/novacept_email_post/css/novacept_email_post.css"
# web_include_js = "/assets/novacept_email_post/js/novacept_email_post.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "novacept_email_post/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "novacept_email_post.utils.jinja_methods",
#	"filters": "novacept_email_post.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "novacept_email_post.install.before_install"
# after_install = "novacept_email_post.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "novacept_email_post.uninstall.before_uninstall"
# after_uninstall = "novacept_email_post.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "novacept_email_post.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"novacept_email_post.novacept_email_post.doctype.novacept_email_post.novacept_email_post.send_email_to_leads_or_contacts",
		"novacept_email_post.novacept_email_post.doctype.novacept_email_post.novacept_email_post.set_email_campaign_status"
	],
}
#	"daily": [
#		"novacept_email_post.tasks.daily"
#	],
#	"hourly": [
#		"novacept_email_post.tasks.hourly"
#	],
#	"weekly": [
#		"novacept_email_post.tasks.weekly"
#	],
#	"monthly": [
#		"novacept_email_post.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "novacept_email_post.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "novacept_email_post.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "novacept_email_post.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"novacept_email_post.auth.validate"
# ]
