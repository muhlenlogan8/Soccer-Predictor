# Titanic survival prediction following video (Kaggle competition)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

titanic_data = pd.read_csv("workspace/train.csv")
print(titanic_data.head())


plot_data = titanic_data.drop(["Name", "Sex", "Ticket", "Cabin", "Embarked"], axis = 1)

# On heatmap, closer to 0 means no correlation, closer to 1 means positive correlation, closer to -1 means negative correlation
# So, we can see that there is a positive correlation between Fare and Survived, and a negative correlation between Pclass and Survived
sns.heatmap(plot_data.corr(), cmap = "YlGnBu")
plt.show()


# Stratified shuffle split to ensure that the training and testing data have the same ratio of survivors to non-survivors
from sklearn.model_selection import StratifiedShuffleSplit

split = StratifiedShuffleSplit(n_splits = 1, test_size = 0.2)
for train_indicies, test_indicies in split.split(titanic_data, titanic_data[["Survived", "Pclass", "Sex"]]):
    strat_train_set = titanic_data.loc[train_indicies]
    strat_test_set = titanic_data.loc[test_indicies]


# Below plots are to show the ratio of survivors to non-survivors in the training and testing data. If the two look similar, we can say that the stratified shuffle split worked
plt.subplot(1, 2, 1)
strat_train_set["Survived"].hist()
strat_train_set["Pclass"].hist()

plt.subplot(1, 2, 2)
strat_test_set["Survived"].hist()
strat_test_set["Pclass"].hist()
plt.show()


# Check for missing values and we see that Age, Cabin, and Embarked have missing values
print(strat_train_set.isnull().sum())

# TrasnsformerMixin is for fit_transform method (mixes fit and transform methods)
from sklearn.base import BaseEstimator, TransformerMixin

# Imputer is we have to replace missing values with something
from sklearn.impute import SimpleImputer

# Fill in missing values for Age
class AgeImputer(BaseEstimator, TransformerMixin):

    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        imputer = SimpleImputer(strategy = "mean")
        X["Age"] = imputer.fit_transform(X[["Age"]])
        return X

# Fill in missing values for Embarked
from sklearn.preprocessing import OneHotEncoder

# Fill in missing values for Embarked and encode categorical data
class FeatureEncoder(BaseEstimator, TransformerMixin):

    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        encoder = OneHotEncoder()

        # Fill in missing values for Embarked
        matrix = encoder.fit_transform(X[["Embarked"]]).toarray()
        column_names = ["C", "S", "Q", "N"]
        for i in range(len(matrix.T)):
            X[column_names[i]] = matrix.T[i]

        # Fill in missing values for Sex
        matrix = encoder.fit_transform(X[["Sex"]]).toarray()
        column_names = ["female", "male"]
        for i in range(len(matrix.T)):
            X[column_names[i]] = matrix.T[i]
        
        return X

# Drop features that we don't need
class FeatureDropper(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        if X is None:
            return None
        return X.drop(["Embarked", "Name", "Ticket", "Cabin", "Sex", "N"], axis = 1, errors = "ignore")
    
# Above is essentially a pipeline in machine learning
# We get the dataset and feed it into the AgeImputer class, which fills in the missing values for Age
# Then, we feed the dataset into the FeatureEncoder class, which fills in the missing values for Embarked and encodes the categorical data
# Finally, we feed the dataset into the FeatureDropper class, which drops the features that we don't need


# Pipeline to fill in missing values for Age, fill in missing values for Embarked and encode categorical data, and drop features that we don't need
from sklearn.pipeline import Pipeline

pipeline = Pipeline([("ageimputer", AgeImputer()), ("featureencoder", FeatureEncoder()), ("featuredropper", FeatureDropper())])

# Run dataset through pipeline
print("\nBefore:")
print(strat_train_set.head())
strat_train_set = pipeline.fit_transform(strat_train_set)
print("\nAfter:")
print(strat_train_set.head())

# Check for missing values and we see that Age, Cabin, and Embarked have NO missing values
print(strat_train_set.isnull().sum())


# Scale the data
from sklearn.preprocessing import StandardScaler

X = strat_train_set.drop(["Survived"], axis = 1)
y = strat_train_set["Survived"]

scaler = StandardScaler()
X_data = scaler.fit_transform(X)
y_data = y.to_numpy()


# Random forest classifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


# clf = RandomForestClassifier()

# Set different parameters to test
# param_grid = [
#     {"n_estimators": [10, 100, 200, 500],
#      "max_depth": [None, 5, 10],
#      "min_samples_split": [2, 3, 4]}
# ]

# Test combinations of parameters and print the best one to use for the final classifier (This takes a while to run)
# Best to use with jupiter notebook where everything is chuncked so this only has to be ran once
# grid_search = GridSearchCV(clf, param_grid, cv = 3, scoring = "accuracy", return_train_score = True)
# grid_search.fit(X_data, y_data)
# final_clf = grid_search.best_estimator_
# print(final_clf)

# Test the final classifier on the test set
# strat_test_set = pipeline.fit_transform(strat_test_set)
# X_test = strat_test_set.drop(["Survived"], axis = 1)
# y_test = strat_test_set["Survived"]

# scaler = StandardScaler()
# X_data_test = scaler.fit_transform(X_test)
# y_data_test = y_test.to_numpy()

# Print the accuracy of the final classifier on the test data
# print(final_clf.score(X_data_test, y_data_test))


# Run titanic_data through pipeline as final_data
final_data = pipeline.fit_transform(titanic_data)

X_final = final_data.drop(["Survived"], axis = 1)
y_final = final_data["Survived"]

scaler = StandardScaler()
X_data_final = scaler.fit_transform(X_final)
y_data_final = y_final.to_numpy()

# Run grid search on final_data to get the best parameters for the final classifier
prod_clf = RandomForestClassifier()

param_grid = [
    {"n_estimators": [10, 100, 200, 500],
     "max_depth": [None, 5, 10],
     "min_samples_split": [2, 3, 4]}
]

grid_search = GridSearchCV(prod_clf, param_grid, cv = 3, scoring = "accuracy", return_train_score = True)
grid_search.fit(X_data_final, y_data_final)

# Print the best parameters for the final classifier
prod_final_clf = grid_search.best_estimator_
print(prod_final_clf)

# Run titanic_test_data through pipeline as final_test_data
titanic_test_data = pd.read_csv("workspace/test.csv")
final_test_data = pipeline.fit_transform(titanic_test_data)

# Fill na with next value in column
X_final_test = final_test_data
X_final_test = X_final_test.fillna(method = "ffill")

# Run final_test_data through the final classifier to get the predictions
scaler = StandardScaler()
X_data_final_test = scaler.fit_transform(X_final_test)

predictions = prod_final_clf.predict(X_data_final_test)

# Create a dataframe with the PassengerId and append the predictions
final_df = pd.DataFrame(titanic_test_data["PassengerId"])
final_df["Survived"] = predictions

# Save the dataframe as a csv file
final_df.to_csv("workspace/titanic_predictions.csv", index = False)

print(final_df)