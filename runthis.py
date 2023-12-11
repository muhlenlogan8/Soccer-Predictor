# Place to run everything prior to implementing taipy stuff

from time import sleep

# Run the scraper (Creates or updates 2 json files)
from scraper import scrape_data
scrape_data()

# Get data from the json files and clean it
from data import get_data
df = get_data()
print(df)

# Do machine learning stuff here using df