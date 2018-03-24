from psycopg2 import connect

# select a row from database - must be ready to query
# check query limit
# choose time to go to work 
# choose time to leave from work
# get driving directions, time, distance - check if results good
# get public transit time, distance - check if results good
# append results to the database
# remove the original result

# connect to the database
conn = connect(database = 'commuter', host = 'localhost')
cur = conn.cursor()

query = """
SELECT 
ID,
latitude,
longitude
FROM craigslistpull
WHERE status = 'cleaned' 
ORDER BY datetime DESC 
LIMIT 1
"""

cur.execute(query)

