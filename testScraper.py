import pandas as pd
from bs4 import BeautifulSoup
import requests

url = "https://www.fifa.com/fifa-world-ranking/men?dateId=id14212"

page_to_scrape = requests.get(url)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

print("Scraping current FIFA ranking")

# Create lists to store the data
ranks = []
teams = []

# Get the table with the ranking data
ranking_table = soup.findAll("tr", attrs = {"class": "row_rankingTableFullRow__Y_A4i"})
print(ranking_table)


for rank in ranking_table:
    ranks.append(ranking_table.find("td", attrs = {"class": "row_rankingTableFullCell__QBdWh row_rank__4Nk3r"}).get_text())
    teams.append(ranking_table.find("td", attrs = {"class": "card-heading-small row_rankingTableFullCell__QBdWh"}).get_text())

print(ranks)