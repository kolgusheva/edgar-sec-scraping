import json
import urllib2
from datetime import datetime
import re
import smtplib
import sqlite3

creds = ''
with open("cred.json", "r") as f:
	creds = json.load(f)

date = datetime.now().strftime("%Y%m%d")

date = "20150625"

url = "ftp://ftp.sec.gov/edgar/daily-index/form." + date + ".idx"

forms = ["D", "8-K", "10-Q", "10-K"]

db = creds["database"]

def connect_db ():
	rv = sqlite3.connect(db)
	rv.row_factory = sqlite3.Row
	return rv

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


def make_url_and_acc(url_txt):
	p = re.compile("(\d{1,})\/(.*)")
	link = url_txt
	result = re.search(p, link)
	#Central index key
	CIK = result.group(1)
	#Accession number 
	ACC_NUM = result.group(2)
	ACC_NUM = ACC_NUM.replace(".txt", "")
	ACC_NUM_NO_DASH = ACC_NUM.replace("-", "")
	ACC_NUM_WITH_INDEX = ACC_NUM + "-index.html"
	FULL_URL = "https://www.sec.gov/Archives/edgar/data/" + CIK + "/" + ACC_NUM_NO_DASH + "/" + ACC_NUM_WITH_INDEX
	to_return = {
		"full_url": FULL_URL,
		"acc_num": ACC_NUM
	}
	return to_return


page = openUrl(url)

matches = []

matches_for_db = []

if page:
	by_lines = page.split("\n")
	by_lines = by_lines[11:]

	total_to_visit = 0

	for line in by_lines:

		p = re.compile( '\s{2,}')
		line = p.sub( ';', line)
		line = line[:-1]
		line_as_list = line.split(";")

		if line_as_list[0] in forms:

			total_to_visit = total_to_visit + 1

	print total_to_visit	


	for line in by_lines:

		p = re.compile( '\s{2,}')
		line = p.sub( ';', line)
		line = line[:-1]
		line_as_list = line.split(";")

		#Line_as_list structure: 
			# lines_as_list[0] - form type
			# lines_as_list[1] - company name
			# lines_as_list[2] - cik
			# lines_as_list[3] - date 
			# lines_as_list[4] - link
			# lines_as_list[5] - state

		if line_as_list[0] in forms:
			total_to_visit = total_to_visit - 1
			print total_to_visit
			detail_url = "ftp://ftp.sec.gov/" + line_as_list[4]
			detail_page = urllib2.urlopen(detail_url).read()
			detail_page_by_lines = detail_page.split("\n")
			if line_as_list[0] == "D":
				state = detail_page_by_lines[18]
			else:
				state = detail_page_by_lines[19]
			state = state[-2:]
			if state == "DE":
				line_as_list.append(state)
				url_and_acc = make_url_and_acc(line_as_list[4])
				line_as_list[4] = url_and_acc["full_url"]
				ass_num = url_and_acc["acc_num"]
				line_as_list.append(ass_num)
				new_line = " --- ".join(line_as_list)
				matches_for_db.append(line_as_list)
				matches.append(new_line)



connection = connect_db()


for row in matches_for_db:
	query = "INSERT INTO filings (type, comp_name, cik, date, link, state, ass_num) VALUES (?,?,?,?,?,?,?)"
	connection.execute(query, row)


connection.commit()






send_email(matches)



# ftp://ftp.sec.gov/edgar/data/845698/0000913849-15-000181.txt
# https://www.sec.gov/Archives/edgar/data/845698/000091384915000183/0000913849-15-000183-index.htm
