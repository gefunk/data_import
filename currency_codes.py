import urllib2
import xml.etree.ElementTree as ET
import MySQLdb


# get file from currency code site
response = urllib2.urlopen('http://www.currency-iso.org/content/dam/isocy/downloads/dl_iso_table_a1.xml')
html = response.read()
root = ET.fromstring(html)


sql = """INSERT INTO currency_codes
		(
			country_name, 
			description, 
			code,
			numeric_code
		) 
		VALUES (%s,%s,%s,%s)"""

rows = []

conn=MySQLdb.connect(host="localhost",user="rahul",passwd="boar",db="rate_management")
cursor = conn.cursor()

for currency in root:
	entity = currency.find('ENTITY').text
	if entity:
		entity = entity.encode('utf-8')
	currency_description = currency.find('CURRENCY').text
	if currency_description:
		currency_description = currency_description.encode('utf-8')
	alphabetic_code = currency.find('ALPHABETIC_CODE').text
	if alphabetic_code:
		alphabetic_code = alphabetic_code.encode('utf-8')
	numeric_code = currency.find('NUMERIC_CODE').text
	minor_unit = currency.find('ENTITY').text
	#print "Description: {0}, code: {1}, numeric code: {2}, minor unit: {3}, Entity: {4}".format(currency_description,alphabetic_code, numeric_code, minor_unit, entity.encode('utf-8'))
	if entity and currency_description and alphabetic_code:
		row = (entity, currency_description, alphabetic_code, numeric_code)
		cursor.execute(sql, row)

conn.commit()
cursor.close()
conn.close()