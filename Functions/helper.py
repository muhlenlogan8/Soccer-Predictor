# data.py helper functions
import pandas as pd

# Modernize countries/teams
def combine_like_countries(df):
    
    # Dictionary of mappings from current country names to the country name that should be used
    team_mapping = {
    "East Germany": "Germany",
    "West Germany": "Germany",
    "Soviet Union": "Russia",
    "FR Yugoslavia": "Serbia",
    "Yugoslavia": "Serbia",
    "Czech Republic": "Czechia",
    "Zaire": "DR Congo",
    "Dutch East Indies": "Indonesia"
    }

    # Apply the mapping to the home_team and away_team columns of the dataframe
    df["away_team"] = df["away_team"].apply(lambda x: team_mapping.get(x, x))
    df["home_team"] = df["home_team"].apply(lambda x: team_mapping.get(x, x))
    return df


# Split Serbia and Montenegro into Serbia and Montenegro
def split_double_countries(df):

    # Helper split_double_countries function
    def split_double_countries_helper(df, name, sub_name1, sub_name2):
        # Create copy of rows with Serbia and Montenegro as home_team and away_team
        temp_home = df[df["home_team"] == name].copy()
        temp_away = df[df["away_team"] == name].copy()

        # Replace Serbia and Montenegro with Montenegro in the temp copies
        temp_home["home_team"] = sub_name2
        temp_away["away_team"] = sub_name2

        # Dictionary to map Serbia and Montenegro to Serbia
        team_mapping = {name: sub_name1}
        
        # Replace Serbia and Montenegro with Serbia in dataframe
        df["away_team"] = df["away_team"].apply(lambda x: team_mapping.get(x, x))
        df["home_team"] = df["home_team"].apply(lambda x: team_mapping.get(x, x))

        # Concatenate the dataframes with the temp copies
        df = pd.concat([df, temp_home, temp_away], ignore_index = True)
        return df

    # Run through helper function
    df = split_double_countries_helper(df, "Serbia and Montenegro", "Serbia", "Montenegro")
    df = split_double_countries_helper(df, "Czechoslovakia", "Czechia", "Slovakia")
    return df


# Stripping of the home_team and away_team columns to remove \xa0 and whitespace
def strip_extras(df):
    
    # Strip the home_team helper function
    def strip_home(row):
        return row["home_team"].strip("\xa0").strip()
    
    # Strip the away_team helper function
    def strip_away(row):
        return row["away_team"].strip("\xa0").strip()
    
    # Apply the respective combine function to the home_team and away_team columns of the dataframe
    df["home_team"] = df.apply(strip_home, axis = 1)
    df["away_team"] = df.apply(strip_away, axis = 1)
    return df


# Clean the names of the countries in the ranks dataframe
def clean_ranks(df):
        
        # Dictionary of mappings from current country names to the country name that should be used
        team_mapping = {
        "IR Iran": "Iran",
        "Korea Republic": "South Korea",
        "Côte d'Ivoire": "Ivory Coast",
        "Bosnia-Herzegovina": "Bosnia and Herzegovina",
        "Korea DPR": "North Korea",
        "Türkiye": "Turkey",
        "China PR": "China",
        "Congo DR": "DR Congo"
        }
    
        # Apply the mapping to the country_full column of the dataframe
        df["team"] = df["team"].apply(lambda x: team_mapping.get(x, x))
        return df


# Clean strings in dataframe
def clean_strings(df, df_ranks):
    
    df = strip_extras(df)
    print("Stripped extras")
    df = combine_like_countries(df)
    print("Combined like countries")
    df = split_double_countries(df)
    print("Split double countries")
    df_ranks = clean_ranks(df_ranks)
    print("Cleaned ranks")
    return df, df_ranks