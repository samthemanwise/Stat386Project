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