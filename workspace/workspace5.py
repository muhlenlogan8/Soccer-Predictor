# Linear regression via video
# Two datasets being used, diabetes and boston housing


# Getting the dataset

from sklearn import datasets
import pandas as pd

# Load the diabetes dataset from sklearn
diabetes = datasets.load_diabetes()

# Load the boston housing dataset from csv file
boston_housing_data = pd.read_csv("workspace\BostonHousing.csv")

# Print description of the diabetes dataset
# print(diabetes.DESCR)
# In the data, the first 10 columns will be used to predict the 11th column

# Create x and y data matricies
# For diabetes dataset, x is the data and y is the target
#x = diabetes.data
#y = diabetes.target

# For boston housing dataset, x is the data and y is the target
# x is all columns other than medv (median value of owner-occupied homes in $1000's)
# y is medv, medv is the target
x = boston_housing_data.drop("medv", axis = 1)
y = boston_housing_data["medv"]

# Print the shape of the data matricies showing number of rows and columns (rows, columns)
# print(x.shape)
# print(y.shape)


# Data splitting

from sklearn.model_selection import train_test_split

# Preforming 80/20 split on the data (80% training, 20% testing)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)

# Print the shape of the data matricies showing number of rows and columns (rows, columns)
# print(x_train.shape)
# print(y_train.shape)


# Linear regression model

from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

# Create a linear regression model
model = linear_model.LinearRegression()

# Build the model using the training data
model.fit(x_train, y_train)

# Make predictions using the testing data
y_pred = model.predict(x_test)

# Prediction results:
# Print the coefficients of the model
print("Coefficients: ", model.coef_)

# Print the intercept of the model
print("Intercept: ", model.intercept_)

# Print the mean squared error of the model
# y_test is the actual values, y_pred is the predicted values
# The best possible score is 0.0 and it can be negative (because the model can be arbitrarily worse)
print("Mean squared error (MSE): %.2f" % mean_squared_error(y_test, y_pred))

# Print the coefficient of determination (R^2) of the model
# The best possible score is 1.0 and it can be negative (because the model can be arbitrarily worse)
# y_test is the actual values, y_pred is the predicted values
print("Coefficient of determination (R^2): %.2f" % r2_score(y_test, y_pred))

# Printing feature names to compare to coefficients
# Diabetes dataset
# print(diabetes.feature_names)

# Boston housing dataset
print(boston_housing_data.columns)

# Diabedes result acts like below
# y = intercept + coef1 * x1 + coef2 * x2 + ... + coef10 * x10  (coef = coefficient, x = feature)

# Boston housing result acts like below
# y = intercept + coef1 * x1 + coef2 * x2 + ... + coef13 * x13  (coef = coefficient, x = feature)


# Plotting the results

import seaborn as sns
import matplotlib.pyplot as plt

# Make a scatter plot and display it
plt.figure(figsize = (15, 8))
# plt.scatter(y_test, y_pred, marker = "+", alpha = 0.5)
plt.scatter(y_test, y_pred, alpha = 0.5)
plt.show()