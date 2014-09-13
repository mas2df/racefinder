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

with open('output.txt', 'r+a') as output_file:

    # Load output file contents into a dict
    output_contents = output_file.readlines()

    # Append date+name to list; Check when adding to list if race already exists in output
    existing_name_date_list = []
    for line in output_contents:
        line_json = json.loads(line)
        blah = line_json["date"] + line_json["name"]
        existing_name_date_list.append(line_json["date"] + line_json["name"])


    race_list = []

    # Iterate over states
    for state in ["VA"]:

        logger.info("State starting: " + state)

        # While loop until there are no results
        page_number = 0 # Start at 0 since we increment before request
        while True:

            # Increase page_number
            page_number = page_number + 1
            logger.info("Retrieving page: " + str(page_number))

            # Build URL with params
            results_page_url = site_url + "State=" + state + "&Page=" + str(page_number)

            # Get the response and soup it up
            response = requests.get(results_page_url)
            soup = bs4.BeautifulSoup(response.text)
            rows = soup.find_all(class_=re.compile(data_row_class_regex))

            # Break out of the while loop
            if len(rows) == 0:
                logger.info("Breaking out of while loop - page: " + str(page_number) + ", state: " + state)
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

                # Check to see if the formatted_date + race_name is already in the content
                if formatted_date + race_name in existing_name_date_list:
                    logger.info("Race already exists: " + formatted_date + " " + race_name)
                    continue

                # Pull out race type
                race_type_list = td_list[2].div.find_all("div")[1].string.split(", ")

                # Get the URL to the race's website
                data_source_url = td_list[2].div.find_all("a")[1]["href"]
                data_source_url = base_url + data_source_url[2:]
                race_site_url = ""
                try:
                    # Follow URL redirect
                    race_site_response = requests.get(data_source_url)
                    for hist in race_site_response.history:
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
                output_file.write("\n")
                race_list.append(race_dict)

        logger.info("State complete: " + state)