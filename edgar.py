import json
import urllib2
from datetime import datetime
import re
import smtplib

creds = ''
with open("cred.json", "r") as f:
	creds = json.load(f)

date = datetime.now().strftime("%Y%m%d")

url = "ftp://ftp.sec.gov/edgar/daily-index/form." + date + ".idx"

forms = ["D", "8-K"]

def openUrl(url):
	try:
		page = urllib2.urlopen(url)
		return page.read()
	except urllib2.URLError:
		return False

def send_email(matches):

	gmail_user = creds["gmail_user"]
	gmail_pwd = creds["gmail_pwd"]
	FROM = creds["from"]
	TO = creds["to"] #must be a list
	SUBJECT = "EDGAR scraping: new MO filings!"
	TEXT = "Today we found " + str(len(matches)) + " matches in EDGAR database\n"
	TEXT = TEXT + "Here are the matches: \n"
	TEXT = TEXT + "\n".join(matches)

	# Prepare actual message
	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
		#server = smtplib.SMTP(SERVER) 
		server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(FROM, TO, message)
		#server.quit()
		server.close()
		print 'successfully sent the mail'
	except:
		print "failed to send mail"


page = openUrl(url)

matches = []

if page:
	by_lines = page.split("\n")
	by_lines = by_lines[11:]
	for line in by_lines:

		p = re.compile( '\s{2,}')
		line = p.sub( ';', line)
		line = line[:-1]
		line_as_list = line.split(";")

		if line_as_list[0] in forms:
			detail_url = "ftp://ftp.sec.gov/" + line_as_list[4]
			detail_page = urllib2.urlopen(detail_url).read()
			detail_page_by_lines = detail_page.split("\n")
			if line_as_list[0] == "D":
				state = detail_page_by_lines[18]
			else:
				state = detail_page_by_lines[19]
			state = state[-2:]
			if state == "MO":
				line_as_list[4] = "ftp://ftp.sec.gov/" + line_as_list[4]
				new_line = " --- ".join(line_as_list)
				matches.append(new_line)


send_email(matches)



ftp://ftp.sec.gov/edgar/data/845698/0000913849-15-000181.txt
https://www.sec.gov/Archives/edgar/data/845698/000091384915000183/0000913849-15-000183-index.htm
