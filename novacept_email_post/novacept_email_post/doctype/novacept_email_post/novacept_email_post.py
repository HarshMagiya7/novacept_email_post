# Copyright (c) 2022, Novacept and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.utils.file_manager import get_file_path
import frappe
from frappe import _
from frappe.core.doctype.communication.email import make
from frappe.model.document import Document
from frappe.utils import add_days, getdate, today, get_datetime
import datetime
import msal
import requests
import json
import re
import base64
import os


class NovaceptEmailPost(Document):
	def validate(self):
		self.set_date()
		self.trial()
		# checking if email is set for lead. Not checking for contact as email is a mandatory field for contact.
		if self.email_campaign_for == "Client":
			self.validate_client()
		self.validate_email_camp_already_exists()
		self.update_status()

	def set_date(self):
		print(f'\n\n\nCurrent\n{frappe.utils.now_datetime() + datetime.timedelta(seconds = 30)}\n\n\n\n')
		print(f'\n\n\n\nStart{frappe.utils.get_datetime(self.start_date)}\n\n\n\n')
		if  frappe.utils.get_datetime(self.start_date) <(frappe.utils.now_datetime()) :
			frappe.throw(_("Scheduled Time must be a future time."))
		# set the end date as start date + max(send after days) in campaign schedule
		send_after_days = []
		campaign = frappe.get_doc("Campaign", self.campaign_name)
		for entry in campaign.get("campaign_schedules"):
			send_after_days.append(entry.send_after_days)
		try:
			self.end_date = add_days(frappe.utils.get_datetime(self.start_date), max(send_after_days))
		except ValueError:
			frappe.throw(
				_("Please set up the Campaign Schedule in the Campaign {0}").format(self.campaign_name)
			)

	def validate_client(self):
		client_email_id = frappe.db.get_value("Client", self.recipient, "email_id")
		if not lead_email_id:
			lead_name = frappe.db.get_value("Client", self.recipient, "customer_name")
			frappe.throw(_("Please set an email id for the Client {0}").format(lead_name))

	def trial(self):
		print(self.last_post_time)
		self.last_post_time = frappe.utils.now_datetime()
		print(self.last_post_time)
	def validate_email_camp_already_exists(self):
		email_camp_exists = frappe.db.exists(
			"Novacept Email Post",
			{
				"campaign_name": self.campaign_name,
				"recipient": self.recipient,
				"status": ("in", ["In Progress", "Scheduled"]),
				"name": ("!=", self.name),
			},
		)
		if email_camp_exists:
			frappe.throw(
				_("The Campaign '{0}' already exists for the {1} '{2}'").format(
					self.campaign_name, self.email_campaign_for, self.recipient
				)
			)
	def update_status(self):
		start_date = getdate(self.start_date)
		end_date = getdate(self.end_date)
		today_date = getdate(today())
		if start_date > today_date:
			self.db_set("status", "Scheduled")
		elif end_date >= today_date:
			self.db_set("status","In Progress")
		elif end_date < today_date:
			self.db_set("status","Completed")


	def update_post_status(self):
		frappe.db.set_value("Novacept Email Post",self.name,"last_post_time",frappe.utils.now_datetime())
		frappe.db.commit()

# called through hooks to send campaign mails to leads
def send_email_to_leads_or_contacts():
	print('start')
	email_campaigns = frappe.get_all(
		"Novacept Email Post", filters={"status": ("not in", ["Unsubscribed", "Completed", "Scheduled"])}
	)
	print(email_campaigns)
	for camp in email_campaigns:
		email_camp = frappe.get_doc("Novacept Email Post", camp.name)
		last_post = email_camp.get("last_post_time")
		campaign = frappe.get_cached_doc("Campaign", email_camp.campaign_name)
		for entry in campaign.get("campaign_schedules"):
			scheduled_date = add_days(email_camp.get("start_date"), entry.get("send_after_days"))
#			last_post = email_camp.get("last_post_time")
			print(last_post)
			if last_post < scheduled_date < frappe.utils.now_datetime():
				print(entry.name)
				print(entry)
				send_mail(entry, email_camp)
				email_camp.update_post_status()
def send_mail(entry, email_camp):

	# MS 365 config
	client_id = '50c30077-9943-431d-ab29-bbde17ee758d'
	client_secret = '_zr8Q~qsf0tQyH51pFLAsAFE1P2r71.JJc~k2bSm'
	tenant_id = '2403bce5-4dae-4017-bf88-e7951c2fc169'

	authority = f"https://login.microsoftonline.com/{tenant_id}"
	app = msal.ConfidentialClientApplication(client_id=client_id,client_credential=client_secret,authority=authority)
	scopes = ["https://graph.microsoft.com/.default"]


	result = None
	result = app.acquire_token_silent(scopes, account=None)

	if not result:
		print("No suitable token exists in cache. Let's get a new one from Azure Active Directory.")
		result = app.acquire_token_for_client(scopes=scopes)

	print(f'Result: {result}\n')


	recipient_list = []
	if email_camp.email_campaign_for == "Client Group":
		client_list = frappe.get_doc('Client Group',email_camp.get('recipient'))
		for i in client_list.clients:
			client = frappe.get_doc('Client',i.client_member)
			if client.email_id:
				recipient_list.append(client.customer_name)
	else:
		recipient_list.append(email_camp.get('recipient'))
#		group = frappe.get_doc(email_camp.email_campaign_for,email_camp.get('recipient'))
#		for member in group.clients:
#			if frappe.db.get_value('Client',member.client_member,'email_id'):
#				recipient_list.append(frappe.db.get_value('Client',member.client_member,'email_id'))
#	else:
#		print(email_camp.email_campaign_for)
#		print(email_camp.get("recipient"))
#		print(email_camp)
#		recipient_list.append(
#			frappe.db.get_value(
#				'Client',email_camp.get("recipient") ,"email_id"
#
#			)
#		)
#	print(f'Recipient: {recipient_list}')

	print(entry.get("email_template"))
	print(entry.get("name"))
	email_template = frappe.get_doc("Email Template", entry.get("email_template"))
	sender = email_camp.get("sender")
	subject = email_template.get("subject")
	body = email_template.get("response")
	print(body)
	print(subject)
	if "access_token" in result:

		for recipient in recipient_list:
			recipient_mail,recipient_subject,recipient_body = personalize_mail(recipient,subject,body)
			endpoint = f'https://graph.microsoft.com/v1.0/users/{sender}/sendMail'
			email_msg = payload_json(recipient_subject,recipient_body,recipient_mail)
#			email_msg = {
#				'Message': {
#					'Subject': recipient_subject,
#					'Body': {
#						'ContentType': "HTML",
#						'Content': recipient_body
#					},
#					'ToRecipients': [
#					{
#						'EmailAddress': {
#							'Address': recipient_mail
#						}
#					}]
#				},
#			'SaveToSentItems': 'true'}

			r= requests.post(endpoint,headers={'Authorization': 'Bearer ' + result['access_token']}, json=email_msg)

			mail = frappe.new_doc('Mails')
			mail.recipient_mail = recipient
			mail.sender = sender
			mail.sent_time = frappe.utils.now_datetime()
			mail.subject = subject
			mail.content = body

			if r.ok:
				print('Sent email successfully')
				mail.doc_status = "SUCCESS"
			else:
				print(r.json())
				mail.status = "FAILED"
				mail.error = r.json()

			mail.save()
	else:
		print('ERROR')
		print(result.get("error"))
		print(result.get("error_description"))
		print(result.get("correlation_id"))

def payload_json(subject,body,email):

	email_msg = {
		'Message': {
			'Subject':subject,
			'Body': {
				'ContentType': "HTML",
				'Content': body
			},
			'ToRecipients': [
			{
				'EmailAddress': {
					'Address': email
				}
			}]
		},
		'SaveToSentItems': 'true'}

#	print(body)
#	print(type(body))
	attached_image = re.findall(r'src="(.*?)"',body)
#	print(f'Attached images {attached_image}')
	if not attached_image:
		return email_msg
	images = []
	for img_file in attached_image:
#		img_file = img.replace('<img src="','')
#		img_file = img_file.replace('">','')
		img_file_path = get_file_path(img_file)
		with open(img_file_path,'rb') as upload:
			media = base64.b64encode(upload.read())
		media = media.decode('utf-8')
		attachment_json = {
			'@odata.type': '#microsoft.graph.fileAttachment',
			'contentBytes':media,
			'name': img_file.replace('/files/',''),
			'contentType': 'image',
			'contentId':img_file.replace('/files/','')
		}
		images.append(attachment_json)
		body = body.replace(img_file,'cid:'+img_file.replace('/files/',''))
	if attached_image:
		email_msg['Message']['attachments'] = images
		email_msg['Message']['Body']['Content'] = body
#	print(email_msg)

	return email_msg

def personalize_mail(client,subject,body):
	mail = frappe.db.get_value('Client',client,'email_id')
	new_subject = placeholder(client,subject)
	new_body = placeholder(client,body)
	return mail,new_subject,new_body
def placeholder(client,text):
	place_holder = re.findall('{{doc.\w+}}', text)
#		print(place_holder)
#		print(0)
	if not place_holder:
		return text
#		print(1)
	values = []
	for var in place_holder:
#			print(var)
		var = var.replace('{{doc.','')
#			print(var)
		var = var.replace('}}','')
#			print(var)
		try:
			value = frappe.db.get_value('Client',client,var)
			values.append(value)
		except:
			values.append(var)
#			print(values)

	for i in range(len(place_holder)):
		text = text.replace(place_holder[i],values[i])
	return text




# called from hooks on doc_event Email Unsubscribe
def unsubscribe_recipient(unsubscribe, method):
	if unsubscribe.reference_doctype == "Novacept Email Post":
		frappe.db.set_value("Novacept Email Post", unsubscribe.reference_name, "status", "Unsubscribed")


# called through hooks to update email campaign status daily
def set_email_campaign_status():
	email_post = frappe.get_all("Novacept Email Post", filters={"status": ("!=", "Unsubscribed")})
	for entry in email_post:
		email_camp = frappe.get_doc("Novacept Email Post", entry.name)
		email_camp.update_status()
