# Place to run everything prior to implementing taipy stuff


# Run the scraper (Creates or updates 2 json files)
from scraper import scrape_data
# scrape_data()

# Get data from the json files and clean it
from data import get_data
df = get_data()

# Prepare the data for the model
from data import prepare_data
df = prepare_data(df)
print(df)

# Do machine learning stuff here using df