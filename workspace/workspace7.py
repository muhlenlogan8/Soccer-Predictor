# Machine learning classification technique with Iris dataset using logistic regression

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style = "white", color_codes = True)

# Load the Iris dataset
iris = pd.read_csv("workspace\iris.csv")


# Get how many different species there are
print(iris["variety"].value_counts())

# Plot the initial data to show the variety based on sepal length and width
sns.FacetGrid(iris, hue = "variety", height = 6).map(plt.scatter, "sepal.length", "sepal.width").add_legend()
# plt.show()


# Map the variety to a number
flower_mapping = {"Setosa": 0 , "Versicolor": 1, "Virginica": 2}
iris["variety"] = iris["variety"].map(flower_mapping)

# Now if variety is 0, it is Setosa, if 1, it is Versicolor and if 2, it is Virginica


# Split the data into input, X, and output, y (target)
X = iris.drop(["variety"], axis = 1)
y = iris["variety"]


# Logistic regression model
from sklearn.linear_model import LogisticRegression

# Initialize model
lr = LogisticRegression()

# Fit the model (train the model)
lr.fit(X, y)


# Check accuracy of the model
print(lr.score(X, y))

# Make predictions
expected = y
predicted = lr.predict(X)
print(predicted)


# Evaluate model preformance
from sklearn import metrics

# Shows the percentage for each variety that was correctly classified
# f1 score is the harmonic mean of precision and recall (Typically look to this for accuracy evaluation)
print(metrics.classification_report(expected, predicted))

# Prints a matrix of the results
print(metrics.confusion_matrix(expected, predicted))