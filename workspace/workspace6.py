# Another machine learning model video
# This contains both linear regression and random forests

# Notes:
# If the target value is continuous, then the model is a regression model
# If the target value is discrete, then the model is a classification model
# The target value being predicted are numerical so we want a regression model
# If the target values were categorical, then we would want a classification model

# Getting The Dataset

import pandas as pd

# The dataset is over the solubility of molecules and is from the Delaney solubility dataset
df = pd.read_csv("workspace\delaney_solubility_with_descriptors.csv")


# Data Preparation

# x is all columns other than logS (log of the solubility of the molecule)
# y is logS, logS is the target
x = df.drop(["logS"], axis = 1)
y = df["logS"]

# Note: We will use the data of x to predict y


# Data Splitting

from sklearn.model_selection import train_test_split

# Preforming 80/20 split on the data (80% training, 20% testing)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)


# Model Building

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Create a linear regression model
lr = LinearRegression()

# Create a random forest model
rf = RandomForestRegressor(max_depth = 2, random_state = 100)

# Build the models using the training data
# Linear regression model
lr.fit(x_train, y_train)
# Random forest model
rf.fit(x_train, y_train)

# Make predictions using the testing data
# Linear regression model
y_lr_train_pred = lr.predict(x_train)
y_lr_test_pred = lr.predict(x_test)
# Random forest model
y_rf_train_pred = rf.predict(x_train)
y_rf_test_pred = rf.predict(x_test)


# Evaluate model preformance

from sklearn.metrics import mean_squared_error, r2_score

# Linear regression model
# Get mean squared error and r2 score for the training data
lr_train_mse = mean_squared_error(y_train, y_lr_train_pred)
lr_train_r2 = r2_score(y_train, y_lr_train_pred)

# Get mean squared error and r2 score for the testing data
lr_test_mse = mean_squared_error(y_test, y_lr_test_pred)
lr_test_r2 = r2_score(y_test, y_lr_test_pred)

# Random forest model
# Get mean squared error and r2 score for the training data
rf_train_mse = mean_squared_error(y_train, y_rf_train_pred)
rf_train_r2 = r2_score(y_train, y_rf_train_pred)

# Get mean squared error and r2 score for the testing data
rf_test_mse = mean_squared_error(y_test, y_rf_test_pred)
rf_test_r2 = r2_score(y_test, y_rf_test_pred)

# Tidy up the results
# Linear regression model
lr_results = pd.DataFrame(["Linear Regression", lr_train_mse, lr_train_r2, lr_test_mse, lr_test_r2]).transpose()
lr_results.columns = ["Method", "Training MSE", "Training R2", "Testing MSE", "Testing R2"]
# Random forest model
rf_results = pd.DataFrame(["Random Forest", rf_train_mse, rf_train_r2, rf_test_mse, rf_test_r2]).transpose()
rf_results.columns = ["Method", "Training MSE", "Training R2", "Testing MSE", "Testing R2"]

# Combine the results
results = pd.concat([lr_results, rf_results]).reset_index(drop = True)

# Print the results
print(results)


# Plotting the results

import matplotlib.pyplot as plt
import numpy as np

# Create scatter plot
plt.scatter(x = y_train, y = y_lr_train_pred, alpha = 0.3, label = "Training data")

# Add line of best fit
z = np.polyfit(y_train, y_lr_train_pred, 1)
p = np.poly1d(z)

# Add line of best fit and labels
plt.plot(y_train, p(y_train), color = "red")
plt.ylabel("Predicted logS")
plt.xlabel("Experimental logS")

# Display the plot
plt.show()