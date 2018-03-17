from psycopg2 import connect
import json
import re

# establish connection
conn = connect(dbname='commuter', host='localhost')

# get the cursor and extract data to be cleaned
cur = conn.cursor()
cur.execute("SELECT datapull FROM craigslistpull WHERE id IS NULL;")
datapull = cur.fetchall()

# link - text - take care to properly escape
# neighborhood - split into binary for all neighborhoods I will consider


def Price(price):
    return float(re.sub('\$', '', price))

def Nbedrooms(nbedrooms):
    # use regex to get the numbers before 'br'
    if nbedrooms != 'NULL':
        try:
            nbedrooms = re.search('[0-9]*br', nbedrooms)[0]
            nbedrooms = re.sub('br', '', nbedrooms)
            return int(nbedrooms)
        except TypeError:
            return None
    else: return None

def Neighborhoods(neighborhoods):
    # return a list of neighborhoods
    neighborhoods = re.sub('[\\(,\\)]', '', neighborhoods)
    if neighborhoods != None:
        neighborhoods = [x.strip() for x in neighborhoods.split('/')]
    return neighborhoods


def LatLon(latlon):
    try: return float(latlon)
    except ValueError: return None


for i in datapull:

    cur = conn.cursor()

    i = i[0]
    rowDict = {}

    # clean the id
    rowDict['id'] = i['id']

    # clean the price
    rowDict['price'] = Price(i['price'])

    # clean the datetime - should be fine
    rowDict['datetime'] = i['datetime']

    # clean the number of rooms
    rowDict['nbedrooms'] = Nbedrooms(i['n. bedrooms'])

    # latitude and longitude
    rowDict['latitude'] = LatLon(i['latitude'])
    rowDict['longitude'] = LatLon(i['longitude'])

    # clean neighborhood
    # Uncertain to best way to handle - JSON? Text? Binary Indicator?
    rowDict['neighborhood'] = json.dumps(Neighborhoods(i['neighborhood']))

    # clean the link
    rowDict['link'] = i['link'].strip()

    query = """                              
    UPDATE craigslistpull
    SET id = %(id)s, 
        datetime = %(datetime)s,
        neighborhood = %(neighborhood)s, 
        price = %(price)s, 
        nbedroom = %(nbedrooms)s,
        link = %(link)s, 
        latitude = %(latitude)s, 
        longitude = %(longitude)s
    WHERE datapull->> 'id' = %(id)s;
    """

    cur.execute(query, rowDict)

conn.commit()
conn.close()