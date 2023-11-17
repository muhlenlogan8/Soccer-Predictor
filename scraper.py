import pandas as pd
from bs4 import BeautifulSoup
import requests

# URL to scrape
url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup'
res = requests.get(url)
content = res.text
soup = BeautifulSoup(content, 'lxml')

match_data = soup.find_all('div', class_ = 'footballbox')

home_team = []
score = []
away_team = []

for match in match_data:
    home_team.append(match.find('th', class_ = 'fhome').get_text())
    score.append(match.find('th', class_ = 'fscore').get_text())
    away_team.append(match.find('th', class_ = 'faway').get_text())

dict_football = {'home_team': home_team, 'score': score, 'away_team': away_team}
df_football = pd.DataFrame(dict_football)

df_football.to_csv('fifa_worldcup_data.csv', index = False)
print('Data saved to CSV file')
print(df_football)