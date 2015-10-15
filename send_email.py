import json
import csv
import gspread
import smtplib
from oauth2client.client import SignedJwtAssertionCredentials as SJAC

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail():

	# Get credentials
	with open('cred.json', 'r') as creds:
		usr = json.loads(creds.read())

	# Get list of email recepients from the Google Spreadsheet
	# Log in first
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = SJAC(usr['client_email'], usr['private_key'], scope)

	gc = gspread.authorize(credentials)
	# Get the sheet
	sheet = gc.open(usr['spreadsheet_name']).sheet1
	cell_list = sheet.col_values(1)
	# TO == email addresses of recipients (extracted from the Spreadsheet,
	# all values in column 1 except for first, which is column name)
	TO = cell_list[1:]

	# clear list of TO to make sure it's proper addresses
	recepients = []
	for email_addr in TO:
		if email_addr != None:
			recepients.append(email_addr)

	# FROM == sender's email address
	FROM = "missourianapps@gmail.com"

	# Create the body of the message (a plain-text and an HTML version).
	# Open the text file for plain text and HTML for hyper-text
	with open('build/send.txt', 'r') as plain_txt:
		text = plain_txt.read()
		number_of_items = len(list(csv.reader(plain_text))) - 1

	with open('build/send.html', 'r') as hyper_text:
		html = hyper_text.read()

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Edgar Scraper: %s match(es)" % number_of_items
	msg['From'] = FROM
	msg['To'] = ', '.join(recepients)

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the message through Gmail
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
		server.ehlo()
		server.starttls()
		server.login(usr['gmail_user'], usr['gmail_pwd'])
		server.sendmail(FROM, TO, msg.as_string())
		# server.quit()
		server.close()
		print 'successfully sent the mail'
	except:
		print "failed to send mail"