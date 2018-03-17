from psycopg2 import connect
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
            return 'NULL'
    else: return 'NULL'

def Neighborhoods(neighborhoods):
    # return a list of neighborhoods
    neighborhoods = re.sub('[\\(,\\)]', '', neighborhoods)
    if neighborhoods != 'NULL':
        neighborhoods = [x.strip() for x in neighborhoods.split('/')]
    return neighborhoods


def LatLon(latlon):
    try: return float(latlon)
    except ValueError: return 'NULL'


for i in datapull:

    cur = conn.cursor()

    i = i[0]
    rowDict = {}

    # clean the id
    rowDict['id'] = int(i['id'])

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
    rowDict['neighborhood'] = Neighborhoods(i['neighborhood'])

    # clean the link
    rowDict['link'] = i['link'].strip()

    print (rowDict)

    query = """                              
    UPDATE commuter
    SET id = {id}, 
        datetime = {datetime},
        neighborhood = {neighborhood}, 
        price = {price}, 
        nbedrooms = {nbedrooms},
        link = {link}, 
        latitude = {latitude}, 
        longitude = {longitude}
    WHERE datapull->> 'id' = {id};
    """.format(rowDict)

    cur.execute(query)

conn.commit()
conn.close()