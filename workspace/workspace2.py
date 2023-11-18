# Importing json file to dataframe
import pandas as pd

# Open json file and set it to dataframe
df = pd.read_json("workspace\quotes.json", orient = "split")

print(df)