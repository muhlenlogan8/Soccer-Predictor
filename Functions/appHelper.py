import pandas as pd

def run_scraper():
    
    from scraper import scrape_data
    scrape_data()


def collect_data():
    
    from data import get_data, prepare_data, get_rank_ref
    df = get_data()
    df = prepare_data(df)
    df_rank_ref = get_rank_ref(df)
    return df, df_rank_ref


def prepare_df_predict(df_rank_ref, df_predict):
    
    # Drop prior ranking columns (This is important for re-running the code every time the button is pressed since it will just continue making new team_rank and opp_rank columns)
    df_predict = df_predict.drop(columns = ["team_rank", "opp_rank"], axis = 1)
    
    # Merge dataframes based on "team" column
    df_merged = pd.merge(df_predict, df_rank_ref, left_on = "team", right_on = "team", how = "left")

    # Rename columns to avoid conflicts
    df_merged = df_merged.rename(columns = {"rank": "team_rank"})

    # Merge again for "opp_rank" column
    df_merged = pd.merge(df_merged, df_rank_ref, left_on = "opponent", right_on = "team", how = "left")
    df_merged = df_merged.rename(columns = {"rank": "opp_rank"})
    
    # Update original dataframe with renamed merged dataframe
    df_predict = df_merged.rename(columns = {"team_x": "team"}).drop(columns = ["team_y"], axis = 1)
    return df_predict


def predict_winner(df, df_rank_ref, df_predict):
    
    from model import model_for_prediction, model_for_accuracy
    acc = model_for_accuracy(df)
    
    pred = model_for_prediction(df, df_predict)
    return pred, acc