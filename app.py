from flask import Flask, render_template
from edgar import getMatches
from database import database, Filings

matches = getMatches()

def updateDB():

	# Update sql database
	db = database()
	try:
		# Create table if does not exist
		db.create_table(Filings)
	except:
		# If table exists, just pass on
		pass
	# save new filings in database
	for filing in matches['matches']:
		new_row = Filings(**filing)
		new_row.save()

app = Flask(__name__)

data = {
	'MATCHES': matches['matches'],
	'DATA': matches['data']
}

@app.route('/')
def index():
    return render_template('index.html', **data)

if __name__ == '__main__':
    app.debug = True
    app.run()