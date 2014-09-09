import requests
import bs4
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

site_url = 'http://runningintheusa.com/Race/List.aspx?Rank=All&State=VA&Page=1'
data_row_class_regex = "MenuGridView(Alternating)?Row"

race_list = []
header_list = ["skip", "date", "race", "location"]

response = requests.get(site_url)
soup = bs4.BeautifulSoup(response.text)
rows = soup.find_all(class_=re.compile(data_row_class_regex))
for row in rows:
    race_dict = {}
    for index, td in enumerate(row.find_all("td")):
        if index < len(header_list) and header_list[index] != "skip":

            # TODO pull out specific info - strip newlines
            raw = td.text
            raw = raw[1:-1]
            race_dict[header_list[index]] = raw

    # Append the race_dict to the list
    race_list.append(race_dict)

logger.info("race_list: " + race_list)