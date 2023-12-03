from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_page(soup):
    ranks = []
    teams = []

    # Get the table with the ranking data
    ranking_table = soup.find_all("tr", class_="row_rankingTableFullRow__Y_A4i")

    for rank in ranking_table:
        ranks.append(rank.find("h6", class_="ff-m-0").get_text())
        teams.append(rank.find("span", class_="d-none d-lg-block").get_text())

    # Print the results
    for r, t in zip(ranks, teams):
        print(f"Rank: {r}, Team: {t}")

# Set up the Selenium webdriver
driver = webdriver.Chrome()  # Make sure you have chromedriver installed and in your PATH
url = "https://www.fifa.com/fifa-world-ranking/men?dateId=id14212"
driver.get(url)

# Wait for the page to load dynamically (adjust the time as needed)
time.sleep(5)

# Iterate through pages
while True:
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Scrape the current page
    scrape_page(soup)

    # Find the "Next Page" button
    next_button = driver.find_element(by = By.CLASS_NAME, value = "button-theme-module_buttonTheme__niHzp")

    # Check if there is a next page
    if "disabled" in next_button.get_attribute("class"):
        break  # No more pages, exit the loop
    
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "onetrust-pc-dark-filter")))

    # Click the "Next Page" button
    next_button.click()

    # Wait for the page to load dynamically (adjust the time as needed)
    time.sleep(5)

# Close the Selenium webdriver
driver.quit()