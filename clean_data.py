import pandas as pd

# Load in 2022-2023 Regular Season Data
# Link: https://www.basketball-reference.com/leagues/NBA_2022_advanced.html

# Read the CSV file into a DataFrame

reg21_22 = pd.read_csv("2021-2022reg.csv")

# Clean Data

reg21_22.drop(index = 0, inplace = True)
columns_to_drop = ["Unnamed: 19", "Unnamed: 24", "Player-additional", "Rk"]
reg21_22.drop(columns=columns_to_drop, axis=1, inplace=True)

reg21_22 = reg21_22[reg21_22["Tm"] != "TOT"]

# Load in 2022-2023 Playoff Data
# Link: https://www.basketball-reference.com/playoffs/NBA_2022_advanced.html

# Read the CSV file into a DataFrame

playoff21_22 = pd.read_csv("2021-2022playoff.csv")

# Clean Data

columns_to_drop = ["Unnamed: 19", "Unnamed: 24", "Player-additional", "Rk"]
playoff21_22.drop(columns=columns_to_drop, axis=1, inplace=True)

#Write clean data to new csv 

reg21_22.to_csv("clean_reg21_22.csv", index = False)
playoff21_22.to_csv("clean_playoff21_22.csv", index = False)


# Read in RAPTOR Dataframe
# Link: https://github.com/fivethirtyeight/data/blob/master/nba-raptor/modern_RAPTOR_by_team.csv

raptor_df = pd.read_csv("modern_RAPTOR_by_team.csv")

#Clean Data

# Specify the columns you want to keep
columns_to_keep = ["player_name","season","season_type","team","poss","mp","raptor_offense","raptor_total",
                   "war_total","war_reg_season","war_playoffs","predator_offense","predator_total"]

# Keep only the specified columns
raptor_df = raptor_df[columns_to_keep]

raptor_df.head()

#Get Just 2021-2022 Season

raptor_df_2022 = raptor_df[raptor_df["season"] == 2022]

raptor_df_2022

## Create Master CSV

# Renaming 'vorp' in data frames so they can join
reg21_22 = reg21_22.rename(columns={'VORP': 'vorp_reg'})

playoff21_22 = playoff21_22.rename(columns={'VORP': 'vorp_post'})

# changing name of player column in raptor to join
raptor_df_2022 = raptor_df_2022.rename(columns={'player_name': 'Player', 'Tm': 'team'})

# Performing the joins
result = pd.merge(raptor_df_2022, reg21_22, on='Player', how='inner')
result = pd.merge(result, playoff21_22, on='Player', how='inner')

columns_to_keep = ['Player', 'season', 'season_type', 'team', 'raptor_total', 'war_total', 'predator_total', 'vorp_reg', 'vorp_post']
result = result[columns_to_keep]
result.to_csv("master.csv", index = False)