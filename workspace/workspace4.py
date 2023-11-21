# Housing prices prediction following video
# Stopped short, poor video but may be of some use

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import the data
data = pd.read_csv("workspace\housing.csv")

# Check the data info
# data.info()

# From the info, we can see that there are 20640 entries and 10 columns.
# Column "total_bedrooms" has 20433 non-null entries, which means there are 207 null entries.
# We can either drop these entries or fill them with the mean value of the column.
# Since it's only 207 entries, we can drop them.
data = data.dropna()

# Above functions same as below
#data.dropna(inplace = True)

# Check the data info
#data.info()

# Now we have 20433 entries and 10 columns

# Want to split the data into training and testing sets
# We can use sklearn's train_test_split function
from sklearn.model_selection import train_test_split

# Split the data into training and testing sets
X = data.drop("median_house_value", axis = 1)
y = data["median_house_value"]

# The train_test_split function spits the data up into the 4 sets X_train, X_test, y_train, y_test
# The test_size parameter determines the size of the testing set so 20% of the data will be used for testing
X_train, X_Test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

# Join X training data with y training data
train_data = X_train.join(y_train)

# Correlation matrix of the data
# train_data.corr()

# Useful to see the correlation matrix as a heatmap
# plt.figure(figsize = (15, 18))
# sns.heatmap(train_data.corr(), annot = True, cmap = "Y1GnBu")
# plt.show()

# Take log of the 4 columns below, resulting in a more normal distribution
train_data["total_rooms"] = np.log(train_data["total_rooms"]) + 1
train_data["total_bedrooms"] = np.log(train_data["total_bedrooms"]) + 1
train_data["population"] = np.log(train_data["population"]) + 1
train_data["households"] = np.log(train_data["households"]) + 1

# Check value count and values of ocean_proximity column
# print(train_data["ocean_proximity"].value_counts())

# Manipulate the ocean_proximity column to binary features
train_data = train_data.join(pd.get_dummies(train_data["ocean_proximity"]))
train_data = train_data.drop("ocean_proximity", axis = 1)

# Now we have multiple columns for ocean_proximity with a 1 value if that row had that proximity and 0 if not

# plt.figure(figsize = (15, 8))
# sns.heatmap(train_data.corr(), annot = True, cmap = "YlGnBu")
# plt.show()

# plt.figure(figsize = (15, 8))
# sns.scatterplot(x = "latitude", y = "longitude", hue = "median_house_value", data = train_data, palette = "coolwarm")
# plt.show()

# Utilizing the above, it can be seen that the scatterplot is a map of California (Based on the data source)
# It can be seen that the houses closer to the coast are more expensive

# Create a new column for the ratio of bedrooms to rooms
train_data["bedroom_ratio"] = train_data["total_bedrooms"] / train_data["total_rooms"]

# Create a new column for the ratio of total rooms to households
train_data["household_rooms"] = train_data["total_rooms"] / train_data["households"]

# plt.figure(figsize = (15, 8))
# sns.heatmap(train_data.corr(), annot = True, cmap = "YlGnBu")
# plt.show()

# Model creation and training
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Create standard scaler object
scaler = StandardScaler()

# Set x_train and y_train
X_train, y_train = train_data.drop("median_house_value", axis = 1), train_data["median_house_value"]

# Scale the input data, don't need to scale the output data
X_train_s = scaler.fit_transform(X_train)

# Create a Linear Regression model
reg = LinearRegression()

# Train the model on the training data
reg.fit(X_train_s, y_train)

# Create test_data by joining X_test and y_test
test_data = X_train.join(y_train)

# Take log of the 4 columns below, resulting in a more normal distribution
test_data["total_rooms"] = np.log(test_data["total_rooms"]) + 1
test_data["total_bedrooms"] = np.log(test_data["total_bedrooms"]) + 1
test_data["population"] = np.log(test_data["population"]) + 1
test_data["households"] = np.log(test_data["households"]) + 1

# Manipulate the ocean_proximity column to binary features
test_data = test_data.join(pd.get_dummies(test_data["ocean_proximity"])).drop("ocean_proximity", axis = 1)

# Create a new column for the ratio of bedrooms to rooms
test_data["bedroom_ratio"] = test_data["total_bedrooms"] / test_data["total_rooms"]
# Create a new column for the ratio of total rooms to households
test_data["household_rooms"] = test_data["total_rooms"] / test_data["households"]

X_test, y_test = test_data.drop("median_house_value", axis = 1), test_data["median_house_value"]

# Scale the input data, don't need to scale the output data
X_test_s = scaler.transform(X_test)

# Check the ISLAND column since there arnen't many entries of it in the original data
# This is important since it could be the case where the ISLAND column isn't present in the
# test data causing an issue with the model when it encounters it in the test data
# print(test_data.ISLAND.value_counts())

# Getting linear regression score
# print(reg.score(X_test, y_test))
print(reg.score(X_test_s, y_test))

#