#!/usr/bin/python
from frozen-app import saveFiles
from send_email import sendEmail

print 'STAGE 1.'
print 'Get data, build HTML content to send.'

saved = saveFiles()

if saved:
	print ''
	print 'STAGE2.'
	print 'Send the actual Email'
	sendEmail()
else:
	print 'Not sendinng email, exiting'