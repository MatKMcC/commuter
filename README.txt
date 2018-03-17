This project came to me as I thought about how the heck I was going to be able to commute to San Mateo and back to San Francisco in a reasonable time frame and how am I going to spend the appropriate amount of money.

The basic idea of the project is to scrape craigslist for apartment data. 
- Price per bedroom
- Address (use lat and long provided in the map)
- Neighborhood
It will be necessary to filter the data on some conditions such as neighborhood and additional validation heuristics. This data can then be plugged into the Google Maps API to generate to and from commute times for Public Transit and Driving.

The ultimate goal of the project will be to identify low cost neighborhoods and low commute time neighborhoods. Additionally, I will be interested in the daily fluctuation of commute times (what is an ideal time to leave and return)

# 1. Scrape Craigslist for data
# 	a. Price per bedroom
#   b. Number of bedrooms
#   c. Price
#   d. Neighborhood
#   e. Lat/Long
#   f. link
# 2. Filter search results down to 
# neighborhood sample size to generate valid estimates
# 3. Setup Google MAPS search query
#   a. Driving Compute Time
#   b. Driving Route
#   c. Public Transit Commute Time
#   d. Public Transit Route
#   e. Commute Start Time
#   f. Commute Finish Time
# 4. Setup Computer in the cloud to run API and store data in
# database