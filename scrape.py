import requests
import bs4

response = requests.get('http://runningintheusa.com/Race/List.aspx?Rank=All&State=VA&Page=1')
soup = bs4.BeautifulSoup(response.text)
links = soup.select('.MenuGridViewHeader')