# get apartment listings from craigslist
from urllib.request import urlopen

baseURL = 'https://sfbay.craigslist.org/d/apts-housing-for-rent/search/apa'


# get the html
response = urlopen(baseURL)
html = response.read()

print (html)

