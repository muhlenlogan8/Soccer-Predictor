# Place to run everything prior to implementing taipy stuff

from scraper import scrape_data
from data import get_data

# Run the scraper (Creates or updates 2 json files)
scrape_data()

# Get data from the json files and clean it
df = get_data()
print(df)

# Do machine learning stuff here using df