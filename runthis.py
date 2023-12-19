# Place to run everything prior to implementing taipy stuff


# Run the scraper (Creates or updates 2 json files)
from scraper import scrape_data
# scrape_data()

# Get data from the json files and clean it
from data import get_data
df = get_data()

# Prepare the data for the model
from data import prepare_data
df, ref = prepare_data(df)
print(df)
print(ref)

# Do machine learning stuff here using df
from modeltest import train_model
prediction_df = train_model(df)
print(prediction_df[prediction_df["won"] != prediction_df["prediction"]])
