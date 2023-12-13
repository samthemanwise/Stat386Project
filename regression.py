import statsmodels.api as sm
import pandas as pd

def lin_regression(reg_df, post_df):
    """
    Performs a linear regression model and gives a summary on our clean and mutated data in order to attempt to predict the 
    performance score of a player's postseason. With the predictive variables being age of a player, regular season performance score,
    league experience in years, and playoff experience in years, as it tries to predict performance score in the playoffs.

    Parameters
    ----------

    reg_df : path 
        Regular season data with metrics and performance score that was created in the wrangle_data module, "reg_norm_metric.csv"

    post_df : path 
        Postseason data with metrics and performance score that was created in the wrangle_data module, "post_norm_metric.csv"

        
    Returns
    -------
    
    Summary of the linear regression that was ran on the data, with the x variables being
    ['Age', 'performance_score', 'years_league', 'years_playoff'] of the regular season data, and the y
    variable will be the 'performance_score' of the postseason data.
    
    """

    # REGRESSION

    # Assuming 'player_name' is the index column, you might need to adjust it
    reg_df.set_index('Player', inplace=True)
    post_df.set_index('Player', inplace=True)

    # Select the common columns for X
    X_columns = ['Age', 'performance_score', 'years_league', 'years_playoff']

    # Align indices and select columns for X
    X = sm.add_constant(reg_df.loc[:, X_columns])

    # Align indices and select columns for Y
    Y = post_df[['performance_score']]

    # Fit the linear regression model
    model = sm.OLS(Y, X)
    results = model.fit()

    # Print the summary
    print(results.summary())