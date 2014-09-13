import requests
import bs4
import logging
import re
import datetime
import json
from utils import states

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

base_url = 'http://runningintheusa.com'
site_url = base_url + '/Race/List.aspx?Rank=All&'
data_row_class_regex = "MenuGridView(Alternating)?Row"
google_geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
google_api_key = 'AIzaSyAIVJmil6fQtb0SYQsq4fgSvduG_vk6WIo'

output_file = open('/Users/michaelsantamaria/Desktop/output.txt', 'r+')
race_list = []

# Iterate over states
for state in ["VA"]:
    # While loop until there are no results
    page_number = 19
    while True:

        # Increase page_number
        page_number = page_number + 1

        # Build URL with params
        full_url = site_url + "State=" + state + "&Page=" + str(page_number)

        # Get the response and soup it up
        response = requests.get(full_url)
        soup = bs4.BeautifulSoup(response.text)
        rows = soup.find_all(class_=re.compile(data_row_class_regex))

        # Break out of the while loop
        if len(rows) == 0:
            logger.info("Breaking out of while loop - page: " + page_number + " - state: " + state)
            break

        # Iterate over rows
        for row in rows:
            td_list = row.find_all("td")

            # Format date: Jan 1, 2014 Wednesday
            race_date_str = td_list[1].get_text().replace("\n", " ").strip()
            race_date_list = re.split("\s*", race_date_str.replace(",", ""))
            race_date_list[1] = race_date_list[1].zfill(2)
            date_obj = datetime.datetime.strptime( " ".join(race_date_list[:3]), "%b %d %Y")
            formatted_date = date_obj.strftime('%Y-%m-%d')

            # Pull out race name and race_types
            race_name = td_list[2].div.find_all("a")[1].string
            race_type_list = td_list[2].div.find_all("div")[1].string.split(", ")

            # Get the URL to the race's website
            data_source_url = td_list[2].div.find_all("a")[1]["href"]
            data_source_url = base_url + data_source_url[2:]
            try:
                # Follow URL redirect
                response = requests.get(data_source_url)
                for hist in response.history:
                    race_site_url = hist.url
            except:
                logger.info("Error retrieving race url: " + data_source_url)

            # Location
            location = td_list[3].a.string
            lonlat = ["", ""]

            if location:
                # Call google geocoding service to get lat lon
                geocode_resp = requests.get(google_geocode_url + location)._content
                geocode_json = json.loads(geocode_resp)
                if geocode_json["results"] and geocode_json["results"][0]:
                    lonlat[0] = geocode_json["results"][0]["geometry"]["location"]["lng"]
                    lonlat[1] = geocode_json["results"][0]["geometry"]["location"]["lat"]

            race_dict = {
                "name": race_name,
                "date": formatted_date,
                "race_type": race_type_list,
                "data_source_url": data_source_url,
                "race_site_url": race_site_url,
                "location": {
                    "full": location,
                    "lon": lonlat[0],
                    "lat": lonlat[1]
                }
            }

            # Append the race_dict to the list
            json.dump(race_dict, output_file)
            race_list.append(race_dict)

        logger.info("race_list: " + str(race_list))