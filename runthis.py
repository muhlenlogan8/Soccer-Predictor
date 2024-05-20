# Place to run everything prior to implementing taipy stuff

# Run the scraper (Creates or updates 2 json files)
from Functions.scraper import scrape_data
scrape_data()

# Get data from the json files and clean it
from Functions.data import get_data
df = get_data()

# Prepare the data for the model
from Functions.data import prepare_data
df = prepare_data(df)
print(df)

# Get the ranking reference dataframe
from Functions.data import get_rank_ref
df_rank_ref = get_rank_ref(df)
print(df_rank_ref)

# Do machine learning stuff here using df
from Functions.modeltest import train_model
prediction_df = train_model(df)
print(prediction_df[prediction_df["won"] != prediction_df["prediction"]])