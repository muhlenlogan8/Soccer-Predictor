import pandas as pd

# Read the csv file into a dataframe
df = pd.read_csv("workspace/matches.csv", index_col = 0)

#print(df.head())

#print(df.shape)
# We have 1389 rows and 27 columns

# Data is for 2 seasons where there are 20 teams and 38 weeks of games so should be 1520 rows

#print(df["team"].value_counts())
# Running the print statement above, we get some teams with 70+ games but some with around 30-40 games
# This is because the data is for 2 seasons and some teams were promoted or relegated between the 2 seasons
# Along with this, Liverpool has data for only 1 season


# Data clean up
# Machine learning algorithms can only work with numerical data so check the dtype of each column
#print(df.dtypes)

# We can see that the date column is an object so we need to convert it to a datetime object
df["date"] = pd.to_datetime(df["date"])


# Create predictor variables

# Did the team play an away game or home game?
df["venue_code"] = df["venue"].astype("category").cat.codes
# What is done above is converting the string into categories then converting the categories into numbers (0 when team is away, 1 when team is home)

df["opp_code"] = df["opponent"].astype("category").cat.codes
# What is done above is converting the opponents string into categories then converting the categories into numbers (Each team now has their own code)

df["hour"] = df["time"].str.replace(":.+", "", regex = True).astype("int")
# What is done above is removing the minutes from the time column and converting the hour into an integer

df["day_code"] = df["date"].dt.dayofweek
# What is done above is getting the day of the week from the date column

df["target"] = (df["result"] == "W").astype("int")
# What is done above is converting the result column into a binary column where 1 is a win and 0 is a loss or draw


# Model
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators = 50, min_samples_split = 10, random_state = 1)
# n_estimators is the number of individual decision trees we want to train. Each decision tree is similar but varies slightly in the parameters
# min_samples_split is the minimum number of samples required to split an internal node. This is used to control over-fitting
# The higher this is, the less likely the model will overfit but the lower the accuracy will be
# random_state is the seed used by the random number generator. This is used to control the randomness of the model
# Setting a random state means if we run the random forest multiple times, we will get the same result if the data is the same

# Set training data as matches prior to 2022
train = df[df["date"] < "2022-01-01"]
# Set testing data as matches in and after 2022
test = df[df["date"] >= "2022-01-01"]

# Set the predictor variables
predictors = ["venue_code", "opp_code", "hour", "day_code"]

# Fit the model
rf.fit(train[predictors], train["target"])

# Generate predictions
preds = rf.predict(test[predictors])

# Determine the accuracy of the model
from sklearn.metrics import accuracy_score

# Accuracy_score is if you predicted a win, what percentage of the time did the team actually win and same for losses (What percentage of the time was your prediction correct)
acc = accuracy_score(test["target"], preds)
print(acc)

# Dig deeper and see when accuracy was high and when it was low
combined = pd.DataFrame({"actual": test["target"], "pred": preds})

print(pd.crosstab(index = combined["actual"], columns = combined["pred"]))

# Precision score metric
from sklearn.metrics import precision_score
# When we predicted a win, what percentage of the time did the team actually win
print(precision_score(test["target"], preds))
# Not great precision

# Create more predictors to improve accuracy
grouped_matches = df.groupby("team")

group = grouped_matches.get_group("Manchester City")

def rolling_averages(group, cols, new_cols):
    group = group.sort_values("date")
    rolling_stats = group[cols].rolling(3, closed = "left").mean() # Combute rolling averages for columns
    group[new_cols] = rolling_stats
    group = group.dropna(subset = new_cols) # Drop rows with missing values
    return group

cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
new_cols = [f"{c}_rolling" for c in cols]

rolling_averages(group, cols, new_cols)

matches_rolling = df.groupby("team").apply(lambda x: rolling_averages(x, cols, new_cols))
# Take original dataframe and group by team. Then apply the rolling averages function to each group (each team)

# This adds an extra index level of the team name so we can drop this
matches_rolling = matches_rolling.droplevel("team")

# We want unique values in our index so we can change this
matches_rolling.index = range(matches_rolling.shape[0])


# Retrain model with new predictors
def make_predictions(data, predictions):
    train = data[data["date"] < "2022-01-01"]
    test = data[data["date"] >= "2022-01-01"]
    rf.fit(train[predictions], train["target"])
    preds = rf.predict(test[predictions])
    combined = pd.DataFrame({"actual": test["target"], "pred": preds})
    precision = precision_score(test["target"], preds)
    return combined, precision

combined, precision = make_predictions(matches_rolling, predictors + new_cols)

print(precision)
# Precision is now 0.625 rather than around 0.48

# Combined doesnt tell us about which team played in each match so we add info to combined
combined = combined.merge(matches_rolling[["date", "team", "opponent", "result"]], left_index = True, right_index = True)
print(combined)

# Look at how algorithm did for both sides of the match
# Algorithm could have predicted that one team wins but also that the other team wins

# Normalize team names
# We do this class thing to ensure .map() doesn't return missing values for teams that aren't in the dictionary below (teams that names are consistent)
class MissingDict(dict):
    __missing__ = lambda self, key: key

map_values = {
    "Brighton and Hove Albion": "Brighton",
    "Manchester United": "Manchester Utd",
    "Newcastle United": "Newcastle Utd",
    "Tottenham Hotspur": "Tottenham",
    "Westham United": "West Ham",
    "Wolverhampton Wanderers": "Wolves",
}

mapping = MissingDict(map_values)
print(mapping["Manchester United"])
print(mapping["Arsenal"])

combined["new_team"] = combined["team"].map(mapping)

# Merge dataframe with itself
merged = combined.merge(combined, left_on = ["date", "new_team"], right_on = ["date", "opponent"])

# Look all rows where one team was predicted to win and the other predicted to lose
print(merged[(merged["pred_x"] == 1) & (merged["pred_y"] == 0)]["actual_x"].value_counts())