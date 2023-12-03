from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

def scrape_page(soup):
    ranks = []
    teams = []

    ranking_table_odd = soup.findAll("tr", attrs = {"class": "odd"})
    ranking_table_even = soup.findAll("tr", attrs = {"class": "even"})

    for rank in ranking_table_odd:
        ranks.append(int(rank.find("td", attrs = {"class": "rank"}).get_text()))
        teams.append(rank.find("td", attrs = {"class": "text team"}).get_text())

    for rank in ranking_table_even:
        ranks.append(int(rank.find("td", attrs = {"class": "rank"}).get_text()))
        teams.append(rank.find("td", attrs = {"class": "text team"}).get_text())

    df = pd.DataFrame({"rank": ranks, "team": teams})
    
    df = df.sort_values(by = "rank").reset_index(drop = True)
    
    # Print the results
    for r, t in zip(ranks, teams):
        print(f"Rank: {r}, Team: {t}")
    return df

# Set up the Selenium webdriver
driver = webdriver.Chrome()  # Make sure you have chromedriver installed and in your PATH
url = "https://us.soccerway.com/teams/rankings/fifa/"
driver.get(url)

# Wait for the page to load dynamically (adjust the time as needed)
time.sleep(5)

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Scrape the current page
df = scrape_page(soup)
print(df)

# Close the Selenium webdriver
driver.quit()