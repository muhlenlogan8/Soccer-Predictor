from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

# Train model with split data to get the accuracy of the model
def model_for_accuracy(df):
    X = df.drop(["won"], axis = 1)
    y = df["won"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    
    model = RandomForestClassifier(n_estimators = 50, min_samples_split = 10, random_state = 1)
    model.fit(X_train.drop(["team", "opponent", "home_score", "opp_score"], axis = 1), y_train)

    preds = model.predict(X_test.drop(["team", "opponent", "home_score", "opp_score"], axis = 1))
    
    acc = accuracy_score(y_test, preds)
    return acc


# Train model with all data to get prediction
def model_for_prediction(df, df_predict):
    X = df.drop(["won"], axis = 1)
    y = df["won"]
    
    model = RandomForestClassifier(n_estimators = 50, min_samples_split = 10, random_state = 1)
    model.fit(X.drop(["team", "opponent", "home_score", "opp_score"], axis = 1), y)

    pred = model.predict(df_predict.drop(["team", "opponent", "home_score", "opp_score"], axis = 1))
    return pred