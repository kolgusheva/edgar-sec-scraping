import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from string import Template


filings = [
	{
		"form_type": '8-K',
		"company_name": "Walmart",
		"cik": '1234567890',
		"date": '11-12-2200',
		'link':'http://google.com',
		'state': 'MO'
	},
	{
		"form_type": '8-K',
		"company_name": "Walmart 2",
		"cik": '1234567890',
		"date": '11-12-2200',
		'link':'http://google.com',
		'state': 'MO'
	},
	{
		"form_type": '8-K',
		"company_name": "Walmart 3",
		"cik": '1234567890',
		"date": '11-12-2200',
		'link':'http://google.com',
		'state': 'MO'
	},
]


form_D_filings = [
	{
		"form_type": 'D',
		"company_name": "World Government",
		"cik": '1234567890',
		"date": '11-12-2200',
		'link':'http://google.com',
		'state': 'MO',
		'offered': '$3',
		'sold': '$50',
		'address': 'Earth',
		'city': 'Mumbai'
	},
	{
		"form_type": 'D',
		"company_name": "World Government 2",
		"cik": '1234567890',
		"date": '11-12-2200',
		'link':'http://google.com',
		'state': 'MO',
		'offered': '$3',
		'sold': '$50',
		'address': 'Earth',
		'city': 'Mumbai'
	},
]



base_html_start = "<html><head></head><body>"
base_html_end = "</table></body></html>"


def send_email(filings, form_D_filings):

	all_forms_table_start = """\
		<table>
			<tr>
				<th>Form Type</th>
				<th>Company Name</th>
				<th>CIK</th>
				<th>Date</th>
				<th>Link</th>
				<th>State</th>
			</tr>"""

	table_end = '</table>'

	form_D_table_start = """\
		<table>
			<tr>
				<th>Form Type</th>
				<th>Company Name</th>
				<th>CIK</th>
				<th>Date</th>
				<th>Link</th>
				<th>State</th>
				<th>Offered</th>
				<th>Sold</th>
				<th>Address</th>
				<th>City</th>
			</tr>"""

	# FROM == my email address
	# TO == recipient's email address
	FROM = "missourianapps@gmail.com"
	TO = ['kolgushev@gmail.com','dorovs@gmail.com']

	TO = ', '.join( TO )

	gmail_user = "missourianapps@gmail.com"
	gmail_pwd = "M@ver!ck$"

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Test HTML - one more!"
	msg['From'] = FROM
	msg['To'] = TO

	# Prepare actual message
	plain_message = "This is a non-HTML version of the email"

	with open('template.html', 'r') as f:
	  all_forms_html = f.read()

	with open('template_form_D.html', 'r') as f:
	  form_D_html = f.read()

	inner_html_list_all_forms = []
	inner_html_list_form_D = []

	for item in filings:
		h = Template(all_forms_html).safe_substitute(item)
		inner_html_list_all_forms.append(h)

	for item in form_D_filings:
			h = Template(form_D_html).safe_substitute(item)
			inner_html_list_form_D.append(h)

	all_forms_html = ''.join(inner_html_list_all_forms)
	form_D_html = ''.join(inner_html_list_form_D)
	
	final_html = base_html_start + all_forms_table_start + all_forms_html + table_end + '<h2>FORM D!!!!</h2>' + form_D_table_start + form_D_html +table_end + base_html_end

	print final_html

	part1 = MIMEText(plain_message, 'plain')
	part2 = MIMEText(final_html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	try:
	#server = smtplib.SMTP(SERVER) 
		server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(FROM, TO, msg.as_string())
		# server.quit()
		server.close()
		print 'successfully sent the mail'
	except:
		print "failed to send mail"



send_email(filings, form_D_filings)