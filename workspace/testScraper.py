from bs4 import BeautifulSoup
import requests

url = "https://us.soccerway.com/teams/rankings/fifa/"

page_to_scrape = requests.get(url)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

print("Scraping current FIFA ranking")

# Create lists to store the data
ranks = []
teams = []

# Get the table with the ranking data
rankings_table = soup.find("table", attrs = {"class": "rankings-container"})
print(rankings_table)

ranking_table_odd = rankings_table.findAll("tr", attrs = {"class": "odd"})
print(ranking_table_odd)
ranking_table_even = rankings_table.findAll("tr", attrs = {"class": "even"})
print(ranking_table_even)

for rank in ranking_table_odd:
    ranks.append(rank.find("td", attrs = {"class": "rank"}).get_text())
    teams.append(rank.find("td", attrs = {"class": "text team"}).get_text())

for rank in ranking_table_even:
    ranks.append(rank.find("td", attrs = {"class": "rank"}).get_text())
    teams.append(rank.find("td", attrs = {"class": "text team"}).get_text())
    
# Print the results
for r, t in zip(ranks, teams):
    print(f"Rank: {r}, Team: {t}")

print("Done")