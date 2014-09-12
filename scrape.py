import requests
import bs4
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

site_url = 'http://runningintheusa.com/Race/List.aspx?Rank=All&State=VA&Page=1'
data_row_class_regex = "MenuGridView(Alternating)?Row"

race_list = []
header_list = ["skip", "date", "race", "location", "link"]

response = requests.get(site_url)
soup = bs4.BeautifulSoup(response.text)
rows = soup.find_all(class_=re.compile(data_row_class_regex))
for row in rows:
    race_dict = {}
    td_list = row.find_all("td")

    date = td_list[1].get_text().replace("\n", "")
    race_name = td_list[2].div.find_all("a")[1].string
    race_type_list = td_list[2].div.find_all("div")[1].string.split(", ")

    race_dict = {
        "date": date,
        "race_name": race_name,
        "type": race_type_list
    }

    # Append the race_dict to the list
    race_list.append(race_dict)

logger.info("race_list: " + str(race_list))