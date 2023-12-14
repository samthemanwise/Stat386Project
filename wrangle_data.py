import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def wrangle_data(reg_csv, post_csv, metric_csv):
    """
    Creates two data frames, one for regular season data and one for postseason data, of the player's season
    that made the playoffs that season dating back to 2014. These data frames are created to contain these variables that 
    are calculated inside the module: player name, age, the season, the season type (RS or PO), RAPTOR metric total, 
    WAR metric total, PREDATOR metric total, league experience in years, playoff experience in years, and a normalized 
    performance score from sum of the three other metrics.

    Parameters
    ----------

    reg_csv : path 
        Clean regular season data for the 2021-2022 CSV that was created in the clean_data module, "clean_reg21_22.csv"

    post_csv : path 
        Clean postseason data for the 2021-2022 CSV that was created in the clean_data module, "clean_playoff21_22.csv"

    metric_csv : path 
        Clean CSV that holds the data for metrics for all players, "modern_RAPTOR_by_team.csv"


    Returns
    -------
    
    Two CSV's, "reg_norm_metric.csv" and "post_norm_metric.csv", that both contain the variables,
    [Player, Age, season, season_type, raptor_total, war_total, predator_total, years_league, years_playoff, performance_score]
    
    """

    # read in data
    reg21_22 = pd.read_csv(reg_csv)
    playoff21_22 = pd.read_csv(post_csv)
    raptor_df = pd.read_csv(metric_csv)

    # Keep specfic columns in raptor
    columns_to_keep = ["player_name","season","season_type","team","poss","mp","raptor_offense","raptor_total",
                       "war_total","war_reg_season","war_playoffs","predator_offense","predator_total"]
    raptor_df = raptor_df[columns_to_keep]

    # change column names and filter by 1000 minutes played
    reg21_22 = reg21_22.rename(columns={'VORP': 'vorp_reg'})
    playoff21_22 = playoff21_22.rename(columns={'VORP': 'vorp_post'})
    reg21_22 = reg21_22[reg21_22['MP'] > 1000]

    # Create master df
    df = pd.DataFrame(raptor_df, columns=['player_name', 'season', 'season_type', 'raptor_total', 'war_total', 'predator_total'])

    # Sorting the dataframe by player and season
    df = df.sort_values(by=['player_name', 'season'])

    # Creating columns for years in the league and years in playoff
    df['years_league'] = df.groupby('player_name').cumcount() + 1
    df['years_playoff'] = df[df['season_type'] == 'PO'].groupby('player_name').cumcount() + 1

    # Filling NaN values in 'years_in_playoff' with 0, indicating no playoff experience in those seasons
    df['years_playoff'] = df['years_playoff'].fillna(0).astype(int)

    # Update 'Years_playoff' for 'RS' rows to match 'PO' rows in the same season
    for index, row in df.iterrows():
        if row['season_type'] == 'RS':
           po_row = df.loc[(df['player_name'] == row['player_name']) & (df['season'] == row['season']) & (df['season_type'] == 'PO')]
           if not po_row.empty:
                df.loc[index, 'years_playoff'] = po_row['years_playoff'].values[0]

    # changing name of player column in raptor to join
    df = df.rename(columns={'player_name': 'Player', 'Tm': 'team'})

    # Performing the joins
    df_merge = pd.merge(df, reg21_22, on='Player', how='inner')
    df_merge = pd.merge(df_merge, playoff21_22, on='Player', how='inner')

    columns_to_keep = ['Player', 'Age_x', 'season', 'season_type', 'raptor_total', 'war_total', 'predator_total', 'years_league', 'years_playoff']
    final = df_merge[columns_to_keep]
    final = final.rename(columns={'Age_x': 'Age'})

    # filter for RS and PO in same year
    final = final.groupby(['Player', 'season']).filter(lambda x: 'RS' in x['season_type'].values and 'PO' in x['season_type'].values)

    # creating normalized general performance metric
    final_reg = final[final['season_type'] == 'RS']
    final_post = final[final['season_type'] == 'PO']

    metrics = ['raptor_total', 'war_total', 'predator_total']  # Replace with actual metric names
    scaler = MinMaxScaler()

    final_reg_norm = final_reg.copy()
    final_post_norm = final_post.copy()

    final_reg_norm[metrics] = scaler.fit_transform(final_reg[metrics])
    final_post_norm[metrics] = scaler.fit_transform(final_post[metrics])

    final_reg_norm['performance_score'] = final_reg_norm[metrics].sum(axis=1)
    final_post_norm['performance_score'] = final_post_norm[metrics].sum(axis=1)

    # Filter out duplicates for players with two 'RS' rows in the same season
    final_reg_norm = final_reg_norm[~((final_reg_norm['season_type'] == 'RS') & final_reg_norm.duplicated(subset=['Player', 'season']))]

    final_reg_norm.to_csv("reg_norm_metric.csv", index = False)
    final_post_norm.to_csv("post_norm_metric.csv", index = False)