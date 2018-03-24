# get apartment listings from craigslist
from urllib.request import urlopen
from scrapeHTML import parseListings
from psycopg2 import connect
from datetime import datetime


# assign unique ID number 

# open connection to the database
conn = connect(dbname='commuter', host='localhost')
cur = conn.cursor()

# establish the connection and get the most recent date 
query = """
SELECT 
datetime
FROM craigslistpull
WHERE datetime IS NOT NULL
ORDER BY datetime
DESC LIMIT 1
"""

cur.execute(query)
date_limit = cur.fetchone()[0]

baseURL = 'https://sfbay.craigslist.org/d/apts-housing-for-rent/search/apa'

results = []
nextpage = ''
iteration = 0

while len(results) % 120 == 0 or iteration == 1: 

	print (iteration * 120)

	# get the html
	response = urlopen(baseURL + nextpage)
	html = response.read()

	# parse the listings for the html
	results += parseListings(html, date_limit)

	# search query look backward in listings
	iteration += 1
	nextpage = '?s={}'.format(iteration * 120)

print (len(results))


# if the date limit is not hit - adjust search constraints and iterate again
# pull most recent date from table --- iterate html until that date is reached
'https://sfbay.craigslist.org/search/apa?s=240'


