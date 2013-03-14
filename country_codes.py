import urllib2
import xml.etree.ElementTree as ET
import MySQLdb


# get file from currency code site
response = urllib2.urlopen('http://www.iso.org/iso/home/standards/country_codes/country_names_and_code_elements_xml.htm')
html = response.read()
root = ET.fromstring(html)


sql = """INSERT INTO country_codes
		(
			name, 
			code
		) 
		VALUES (%s,%s)"""

rows = []

conn=MySQLdb.connect(host="localhost",user="rahul",passwd="boar",db="rate_management")
cursor = conn.cursor()

for country in root:
	name = country.find('ISO_3166-1_Country_name').text
	if name:
		name = name.encode('utf-8')
	code = country.find('ISO_3166-1_Alpha-2_Code_element').text
	if code:
		code = code.encode('utf-8')
	#print "Description: {0}, code: {1}, numeric code: {2}, minor unit: {3}, Entity: {4}".format(currency_description,alphabetic_code, numeric_code, minor_unit, entity.encode('utf-8'))
	if name and code:
		row = (name, code)
		cursor.execute(sql, row)

conn.commit()
cursor.close()
conn.close()