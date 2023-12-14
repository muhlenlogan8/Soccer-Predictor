from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

def train_model(df):
    
    X = df.drop(["won"], axis = 1)
    y = df["won"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    
    model = RandomForestClassifier(n_estimators = 50, min_samples_split = 10, random_state = 1)
    
    model.fit(X_train.drop(["team", "opponent"], axis = 1), y_train)
    
    preds = model.predict(X_test.drop(["team", "opponent"], axis = 1))

    acc = accuracy_score(y_test, preds)
    print(acc)
    
    prediction_df = pd.concat([X_test, y_test], axis = 1)
    prediction_df["prediction"] = preds
    return prediction_df