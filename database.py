from peewee import *

db = SqliteDatabase('db.sqlite')

# Setting up db table
class Filings(Model):

	form = CharField()
	name = CharField()
	date = DateField()
	cik = IntegerField()
	url  = CharField()
	acc_num = CharField()
	street_address = CharField()
	city = CharField()
	type_of_securities = CharField()
	type_of_filing = CharField()
	total_offering = IntegerField()
	total_sold = IntegerField()
	industry = CharField()
	signer_name = CharField()
	signer_title = CharField()

	class Meta:
		database = db # this model uses the "db.sqlite" database

def database():
	db.connect()
	return db