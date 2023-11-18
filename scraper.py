import pandas as pd
from bs4 import BeautifulSoup
import requests

# URL to scrape
url = "https://en.wikipedia.org/wiki/2022_FIFA_World_Cup"
page_to_scrape = requests.get(url)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

match_data = soup.findAll("div", attrs = {"class": "footballbox"})

home_team = []
away_team = []
game_score = []
pk_score = []

for match in match_data:
    home_team.append(match.find("th", attrs = {"class": "fhome"}).get_text())
    away_team.append(match.find("th", attrs = {"class": "faway"}).get_text())
    score = match.find("th", attrs = {"class": "fscore"}).get_text()
    game_score.append(score)

    if "a.e.t." in score:
        home_pk_score = 0
        away_pk_score = 0
        match_home_pks = match.find_all("td", attrs = {"class": "fhgoal"})
        match_away_pks = match.find_all("td", attrs = {"class": "fagoal"})
        
        home_pk_score = len(match_home_pks[1].find_all("span", attrs = {"title": "Penalty scored"}))
        away_pk_score = len(match_away_pks[1].find_all("span", attrs = {"title": "Penalty scored"}))

        pk_score.append(str(home_pk_score) + "-" + str(away_pk_score))
    else:
        pk_score.append("N/A")

dict_football = {"home_team": home_team, "game_score": game_score, "pk_score": pk_score, "away_team": away_team}
df_football = pd.DataFrame(dict_football)

df_football.to_json("data.json", orient = "split")