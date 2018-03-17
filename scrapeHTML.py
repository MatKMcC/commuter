# in this we want to be able to run to append postings to a
# dataset. We will need match existing postings and not append
# for the first time run, examine postings as old as a week
# for additional run time only gather postings within 24 hours


# get a list of URLs - SELENIUM
# --- a. given a start link,
# https://sfbay.craigslist.org/d/apts-housing-for-rent/search/apa
#        scrape links and click next until
#        stopping condition is met
# results are
# iterate through URLs to parse information
# store in a postgres database


# given this - https://sfbay.craigslist.org/d/apts-housing-for-rent/search/apa
# get the following
# ---> date
# ---> neighborhood
# ---> link
# ---> price
# ---> n. bedrooms
# follow the link
# get the following
# ---> latitude
# ---> longitude

# create table query - add text to create if does not exist, append if does
# add data validation -- make sure there are no duplicates
# CREATE TABLE craigslistpull ( id BIGINT, datetime TIMESTAMP, neighborhood JSON, nbedroom INT, price DOUBLE PRECISION, link TEXT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, datapull JSON )


# use beautifulsoup to parse
from bs4 import BeautifulSoup
from psycopg2 import connect
import requests
import json

f = open('exampleRootPage.html')
html = f.read()


def testSoup(soupRequest, text = True):
    """
    Could be better...ad hoc error handling for missing values in
    craigslist listings. Most relevant to calling the text
    attribute on a nonetype due to missingness of tags

    :param soupRequest: a beautiful soup object with
    :param text: if the object requires text extraction
    :return: the expected extraction or 'NULL'
    """

    try:
        if text == True: return soupRequest.text if soupRequest else 'NULL'
        else: return soupRequest.text if soupRequest else 'NULL'
    except AttributeError: return 'NULL'


def parseListings(htmlString):
    """
    Parse the listings from a page of Craigslist results
    :param htmlString: A string of html
    :return: a list of dictionaries with listing information
    """
    soup = BeautifulSoup(htmlString, 'lxml')

    # extract all of the results
    listings = soup.find_all('p', class_='result-info')

    # iterate through results and build an array of dictionaries
    results = []
    for l in listings:
        result = {}
        result['id'] = l.find('a')['data-id']
        result['link'] = l.find('a')['href']
        result['price'] = testSoup(l.find(class_='result-price'), text=True)
        result['n. bedrooms'] = testSoup(l.find(class_='housing'), text=True)
        result['neighborhood'] = testSoup(l.find(class_='result-hood'), text=True)
        result['datetime'] = l.find('time')['datetime']
        results.append(result)

    return results

def extractLatLon(url):
    # open the url
    response = requests.get(url).text
    # extract lat lon
    soup = BeautifulSoup(response, 'lxml')
    map = soup.find('div', class_='viewposting')
    try: return map['data-latitude'], map['data-longitude']
    except TypeError: return 'NUll', 'NULL'

def insertDataQuery(listings,tablename):

    query = 'INSERT INTO %s ( %s ) VALUES' % (tablename, 'datapull')

    values = []
    q = []

    for l in listings:

        # insert all values formatted as '( json )'
        values.append( json.dumps(l) )
        q.append('( %s )')

    # attach the values to the query statement
    query += ', '.join(q) + ';'

    return query, values


def insertIntoDatabase(dbName, listings):

    # write json files to database
    conn = connect(dbname='commuter', host='localhost')
    cur = conn.cursor()

    # generate query from listings
    query, values = insertDataQuery(listings, 'craigslistpull')

    # insert the query
    cur.execute(query, values)

    # complete the transaction
    conn.commit()


# parse data from listings
listings = parseListings(html)

# for each link in the listings - extract latitude and longitude
for l in listings:
    if extractLatLon(l['link']):
        lat, lon = extractLatLon(l['link'])
        l['latitude'] = lat
        l['longitude'] = lon


# insert the file into a database
insertIntoDatabase('commuter', listings)