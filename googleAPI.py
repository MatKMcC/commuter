
from urllib.parse import quote
from urllib import request
import json

terms = {
    'key' : 'AIzaSyB9CAgUoyktVZFqfa8lNQT2A_Maa-0TdX0',
    'destination' : quote('101 S Ellsworth Ave, San Mateo, CA 94401'),
    'lat' : quote('37.834560'),
    'lon' : quote('-122.197230')
}



# build the url
url = 'https://maps.googleapis.com/maps/api/directions/json?'\
           'origin={lat},{lon}&' \
           'destination={destination}&' \
           'key={key}'.format(**terms)



with request.urlopen(url) as response:
    googleJSON = response.read()


googleResponse = json.loads(googleJSON)

# send the url
# get the response
# parse the response
