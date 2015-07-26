from flask.ext.frozen import Freezer
from app import updateDB, app
from pynliner import fromString

updateDB()
freezer = Freezer(app)

# Create static html files
if __name__ == '__main__':
    freezer.freeze()

with open('build/index.html','r') as html:
	output = fromString(html.read())

with open('build/send.html','w') as send_file:
	send_file.write(output)