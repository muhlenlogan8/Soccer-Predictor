# Learning to Scrape, and output to json, also have a progress bar for fun
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd

# Create overall quotes and author lists
quotesList = []
authorsList = []

# Utilizing tdqm to show progress bar for fun
for i in tqdm(range(1, 11), desc = "Scraping Pages"):
    # Get page to scrape, going from page 1 to 10 of the site
    page_to_scrape = requests.get("https://quotes.toscrape.com/page/" + str(i) + "/")
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")

    # Pull quotes from site
    # To do so, inspect the quotes on the site to see they are represetned by the tag "span" with the class "text"
    quotes = soup.findAll("span", attrs = {"class": "text"})
    for quote in quotes:
        quotesList.append(quote.text)   # Note: .text pulls string rather than array so json works properly

    # Do the same for authors, tag is "small" with class "author"
    authors = soup.findAll("small", attrs = {"class": "author"})
    for author in authors:
        authorsList.append(author.text)

# Print the quote then author following utilizing the combining of the list using zip()
# for quote, author in zip(quotesList, authorsList):
#     print(quote.text + " - " + author.text)

# Create pandas dataframe to house quotes and authors
df = pd.DataFrame({"Quotes": quotesList, "Authors": authorsList})

# Output dataframe to json file
df.to_json("workspace\quotes.json", orient = "split")