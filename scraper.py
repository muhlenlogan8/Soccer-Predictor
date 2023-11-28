import pandas as pd
from bs4 import BeautifulSoup
import requests

# Weird things to note:
# Some years prior used golden goal which is no longer used (This is listed as "(a.e.t./g.g.)" in the score column)
# Some years prior (Found in 1954) allow extra time during group stage matches that result in ties if no winner is found after the extra time
# This is "awesome" because it means there are "(a.e.t.)" entries in the score column but no penalties were taken so I must account for this
# It also seems that some years don't even show the penalty results in the table I'm pulling from
# I may compensate for this by checking which team has a game after the fact but there may be a better way
# Another awesome thing, in 1938, Austria withdrew from the tournament so the match they were supposed to play was a walkover, which is listed as "w/o[a]" in the score column
# Fun history: Nazi Germany invaded and annexed Austria three months before the 1938 world cup and forced 5 Austrian players to play for the German team
# Germany ended up losing their match anyways

# TODO: Account for years such as 1938 where the penalty kick results are not shown in the table I am pulling from
# Currently this year is in trouble_years and the penalty kick results are set to "N/A" for all matches in this year
# Must identify if the match went to penalties or not and if it did, find the penalty kick results from another source
# Nowing if the match is a group stage match or not will help since group stage (a.e.t.) matches didn't go to penalties but later matches did

# List of world cup years
world_cup_years = ["2018", "2014", "2010", "2006", "2002", "1998", "1994", "1990", "1986", "1982", "1978", "1974", "1970", "1966", "1962", "1958", "1954", "1950", "1938", "1934", "1930"]

# List of years that have the weird extra time during group stage matches
trouble_years = ["1954", "1938", "1934"]

# Initialize final dataframe
df_football_final = pd.DataFrame()

# Go through each world cup year and scrape the data
for year in world_cup_years:
    print("Scraping " + year + " World Cup")

    # Make URL to scrape
    url = "https://en.wikipedia.org/wiki/" + year + "_FIFA_World_Cup"

    # Get the page
    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")

    # Get the match data from the page. This data is found in the div with class "footballbox"
    match_data = soup.findAll("div", attrs = {"class": "footballbox"})

    # Create lists to store the data
    year_list = []
    home_team = []
    away_team = []
    game_score = []
    pk_score = []


    for match in match_data:
        # Get the score for the match
        score = match.find("th", attrs = {"class": "fscore"}).get_text()

        # Check if the match was a walkover and skip it if it was
        if score != "w/o[a]":
            # Add the year, home team, away team, and score to their respective lists
            year_list.append(year)
            home_team.append(match.find("th", attrs = {"class": "fhome"}).get_text())
            away_team.append(match.find("th", attrs = {"class": "faway"}).get_text())
            game_score.append(score)

            # Break up score into home and away scores to determine if game went to penalties or not when "a.e.t." is in the score
            home_score, away_score = 0, 0
            if "(a.e.t.)" in score:
                home_score, away_score = map(int, score.replace(" (a.e.t.)", "").replace("–", "-").split("-"))

            # Check if the match went to penalties and get the penalties score in another list, N/A if the match didn't go to penalties
            if "(a.e.t.)" in score and home_score == away_score and year not in trouble_years:
                home_pk_score = 0
                away_pk_score = 0
                match_home_pks = match.find_all("td", attrs = {"class": "fhgoal"})
                match_away_pks = match.find_all("td", attrs = {"class": "fagoal"})
                
                home_pk_score = len(match_home_pks[1].find_all("span", attrs = {"title": "Penalty scored"}))
                away_pk_score = len(match_away_pks[1].find_all("span", attrs = {"title": "Penalty scored"}))

                pk_score.append(str(home_pk_score) + "-" + str(away_pk_score))
            else:
                pk_score.append("N/A")

    # Create a dictionary to store the data
    dict_football = {"year": year_list, "home_team": home_team, "game_score": game_score, "pk_score": pk_score, "away_team": away_team}

    # Create a dataframe from the dictionary
    df_football = pd.DataFrame(dict_football)

    # Add the year's dataframe to final dataframe
    df_football_final = pd.concat([df_football_final, df_football])

# Save the dataframe to a json file
df_football_final.to_json("data.json", orient = "split")