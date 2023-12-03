import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Scrapes world cup match data and saves it to a json file
def scrape_match_data():
    # List of world cup years
    world_cup_years = ["2022", "2018", "2014", "2010", "2006", "2002", "1998", "1994", "1990", "1986", "1982", "1978", "1974", "1970", "1966", "1962", "1958", "1954", "1950", "1938", "1934", "1930"]

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
        home_score_list = []
        away_score_list = []
        pk_score = []

        # Go through each match and get the data
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

                # Break up score into home and away scores
                # home_score, away_score = 0, 0
                # if "(a.e.t.)" in score:
                #     home_score, away_score = map(int, score.replace(" (a.e.t.)", "").replace("–", "-").split("-"))
                home_score, away_score = map(int, score.replace("Awarded[note 1]", "").replace(" (a.e.t./g.g.)", "").replace(" (a.e.t.)", "").replace("–", "-").split("-"))
                home_score_list.append(home_score)
                away_score_list.append(away_score)

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
        dict_football = {"year": year_list, "home_team": home_team, "home_score": home_score_list, "game_score": game_score, "away_score": away_score_list, "pk_score": pk_score, "away_team": away_team}

        # Create a dataframe from the dictionary
        df_football = pd.DataFrame(dict_football)

        # Add the year's dataframe to final dataframe
        df_football_final = pd.concat([df_football_final, df_football])

    # Save the dataframe to a json file
    df_football_final.to_json("match_data.json", orient = "split")
    print("Done scraping match data")


def scrape_ranking_data():
    # Set up the Selenium webdriver
    driver = webdriver.Chrome()
    url = "https://us.soccerway.com/teams/rankings/fifa/"
    driver.get(url)

    # Wait for the page to load
    time.sleep(1)

    # Parse the HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Close the Selenium webdriver
    driver.quit()

    print("Scraping current FIFA ranking")
    
    # Create lists to store the data
    ranks = []
    teams = []

    # Get the tables with the ranking data (two tables due to strange website html names)
    ranking_table_odd = soup.findAll("tr", attrs = {"class": "odd"})
    ranking_table_even = soup.findAll("tr", attrs = {"class": "even"})

    # Add the odd data to the lists
    for rank in ranking_table_odd:
        ranks.append(int(rank.find("td", attrs = {"class": "rank"}).get_text()))
        teams.append(rank.find("td", attrs = {"class": "text team"}).get_text())

    # Add the even data to the lists
    for rank in ranking_table_even:
        ranks.append(int(rank.find("td", attrs = {"class": "rank"}).get_text()))
        teams.append(rank.find("td", attrs = {"class": "text team"}).get_text())

    # Create a dataframe from the lists
    df_rank = pd.DataFrame({"rank": ranks, "team": teams})
    
    # Sort the dataframe by rank and reset the index
    df_rank = df_rank.sort_values(by = "rank").reset_index(drop = True)

    print("Done scraping ranking data")
    # Save the dataframe to a json file
    df_rank.to_json("rank_data.json", orient = "split")
    
    
def scrape_data():
    scrape_match_data()
    scrape_ranking_data()