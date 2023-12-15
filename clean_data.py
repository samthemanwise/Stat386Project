import pandas as pd

def clean_data(reg_csv, post_csv):
    """
    Cleans the two dataframes of the 2021-2022 data, both regular and postseason, that is taken from Basketball-Reference.

    Parameters
    ----------

    reg_csv : path 
        Regular season data for the 2021-2022 NBA season from basketball reference, "2021-2022reg.csv"

    post_csv : path 
        Postseason data for the 2021-2022 NBA season from basketball reference, "2021-2022playoff.csv"


    Returns
    -------
    
    Two clean CSV's, "clean_reg21_22.csv" and "clean_playoff21_22.csv", that both contain the variables,
    [Player,Pos,Age,Tm,G,MP,PER,TS%,3PAr,FTr,ORB%,DRB%,TRB%,AST%,
    STL%,BLK%,TOV%,USG%,OWS,DWS,WS,WS/48,OBPM,DBPM,BPM,VORP]
    
    """

    # Load in 2022-2023 Regular Season Data
    # Link: https://www.basketball-reference.com/leagues/NBA_2022_advanced.html

    # Read the CSV file into a DataFrame

    reg21_22 = pd.read_csv(reg_csv)

    # Clean Data

    reg21_22.drop(index = 0, inplace = True)
    columns_to_drop = ["Unnamed: 19", "Unnamed: 24", "Player-additional", "Rk"]
    reg21_22.drop(columns=columns_to_drop, axis=1, inplace=True)

    reg21_22 = reg21_22[reg21_22["Tm"] != "TOT"]

    # Load in 2022-2023 Playoff Data
    # Link: https://www.basketball-reference.com/playoffs/NBA_2022_advanced.html

    # Read the CSV file into a DataFrame

    playoff21_22 = pd.read_csv(post_csv)

    # Clean Data

    columns_to_drop = ["Unnamed: 19", "Unnamed: 24", "Player-additional", "Rk"]
    playoff21_22.drop(columns=columns_to_drop, axis=1, inplace=True)

    # Write clean data to new csv 

    reg21_22.to_csv("clean_reg21_22.csv", index = False)
    playoff21_22.to_csv("clean_playoff21_22.csv", index = False)