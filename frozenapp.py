from flask.ext.frozen import Freezer
from pynliner import fromString
import csv


def saveFiles():
	from app import updateDB, app, matches

	if matches:
		matches = matches['matches']
		print matches
		updateDB()
		freezer = Freezer(app)
		# Create static html files
		if __name__ == '__main__':
		    freezer.freeze()

		with open('build/index.html','r') as html:
			output = fromString(html.read())

		with open('build/send.html','w') as send_file:
			send_file.write(output)

		with open('build/send.txt','wb') as f:
			keys = matches[0].keys()
			dict_writer = csv.DictWriter(f, keys)
			dict_writer.writeheader()
			dict_writer.writerows(matches)
		return True
	else:
		print 'Looks like something wrong with date in initial URL, nothing saved'
		return False
