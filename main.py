from taipy import Gui
from Functions.appHelper import collect_data, predict_winner, prepare_df_predict
import datetime
import pandas as pd

df, df_rank_ref = collect_data()
df_tbl = df.copy()
teams = sorted(df_rank_ref["team"].tolist())
value1 = ""
value2 = ""
value3 = ""
year = datetime.date.today().year
df_predict = pd.DataFrame({"year": [year], "team": [""], "team_rank": [0], "home_score": [0], "opp_score": [0], "opponent": [""], "opp_rank": [0]})
df_predict_tbl = pd.DataFrame()
pred = -1
acc = -1


page = """
# Soccer Predictor

<|toggle|theme|>

<|{value1}|selector|lov={teams}|dropdown|label="Select Home Team"|>
<|{value2}|selector|lov={teams}|dropdown|label="Select Away Team"|>

<|button1|button|on_action=button_pressed|label="Predict Winner"|>

<|{value3}|>

<|{df_predict_tbl}|table|rebuild=True|>

<|{df_tbl}|table|rebuild=True|>
"""


def on_change(state, var_name, var_value):
    
    if var_name == "value1":
        state.value1 = var_value
    elif var_name == "value2":
        state.value2 = var_value


def button_pressed(state):
    
    state.value3 = "Predicting..."
    state.df_predict["team"] = state.value1
    state.df_predict["opponent"] = state.value2
    state.df_predict = prepare_df_predict(state.df_rank_ref, state.df_predict)
    state.df_predict_tbl = state.df_predict.drop(columns = ["home_score", "opp_score"], axis = 1)
    state.df_predict_tbl = state.df_predict_tbl[["year", "team", "team_rank", "opponent", "opp_rank"]]

    state.df_tbl = state.df[state.df["team"].isin([state.value1, state.value2])]
    
    state.pred, state.acc = predict_winner(state.df, state.df_rank_ref, state.df_predict)
    if state.pred == 1:
        state.value3 = "The model predicts " + state.value1 + " will win with an accuracy of " + str(round(state.acc*100)) + "%"
    elif state.pred == 0:
        state.value3 = "The model predicts " + state.value2 + " will win with an accuracy of " + str(round(state.acc*100)) + "%"
    else:
        state.value3 = "Error"


Gui(page = page).run(use_reloader = False, debug = False, title = "Soccer Predictor")