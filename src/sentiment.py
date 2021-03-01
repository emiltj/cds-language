#!/usr/bin/python

# Importing all the necessary modules
import os
import re
import datetime
import matplotlib.pyplot as plt
import numpy as np
import glob
import pandas as pd
from pathlib import Path
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
spacy_text_blob = SpacyTextBlob()
nlp = spacy.load("en_core_web_sm")



# Importing the dataset
df = pd.read_csv(os.path.join("..", "data", "abcnews-date-text.csv"))
df = df.iloc[0:10001, :]



# Converting dates to datetime format
def convert_to_datetime(df, date_col):
    
    # Creating an empty list which is going to contain the dates in date format instead of numerical
    dates = []
    
    # For each index, and each row in df
    for index, row in df.iterrows():
        
        # take the publish_date and convert to string
        date = str(row[date_col])

        # use datetime.date to make the date into datetime, using indices
        date = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
        
        # append to "dates" list
        dates.append(date)
        
    # overwrite the column "publish_date" with the new dates in datetime format.
    df[date_col] = dates




# Calculate sentiment scores for each headline
def calc_sentiment(df, text_col):

    # Calculate polarity for all headlines and add the polarity score to the dataframe
    sentiment_score = []
    for doc in nlp.pipe(df[text_col]):
        score = doc._.sentiment.polarity
        sentiment_score.append(score)

    df["sentiment_score"] = sentiment_score




# Calculate daily average sentiment scores. Also smoothed scores
def calc_daily_avg_sentiment(df, date_col, sentiment_score_col):
    # Get a list of all unique dates in the dataframe
    unique_dates = list(pd.unique(df[date_col]))

    # Create a new dataframe, with a row for each unique date. Also calculate the mean polarity score for each unique date
    df_dates = pd.DataFrame()
    daily_mean_polarity_score = []

    # For each unique date, get the mean of all sentiment scores, and store it in "daily_mean_polarity_score"
    for unique_date in unique_dates:
        df_for_date_n = df.loc[df[date_col] == unique_date]
        mean_for_date_n = np.mean(df_for_date_n[sentiment_score_col])
        df_dates["date"] = unique_dates
        daily_mean_polarity_score.append(mean_for_date_n)

    # Create a new column with the daily mean polarity scores
    df_dates["daily_mean_polarity_score"] = daily_mean_polarity_score

    # Calculate smoothed mean scores for each date, using a window of 7 days
    daily_polarity_score_weekly_smooth = pd.Series(df_dates["daily_mean_polarity_score"]).rolling(7).mean()

    # Calculate smoothed mean scores for each date, using a window of 30 days  
    daily_polarity_score_monthly_smooth = pd.Series(df_dates["daily_mean_polarity_score"]).rolling(30).mean()

    # Add the smoothed data to the df_dates
    df_dates["daily_polarity_score_weekly_smooth"] = daily_polarity_score_weekly_smooth
    df_dates["daily_polarity_score_monthly_smooth"] = daily_polarity_score_monthly_smooth

    return df_dates




# Plotting the scores
def plot_sentiment(df, start_date, col_no_smooth, col_smooth_7_days, col_smooth_30_days, save = False):
    
    # Adding a figure which is large enough for multiple subplots
    fig = plt.figure(figsize = (24.0, 10.0))

    # Adding subplots
    axes_1 = fig.add_subplot(2,3,2) # 2 rows, 3 columns, 2nd position
    axes_2 = fig.add_subplot(2,3,4) # 2 rows, 3 columns, 4th position
    axes_3 = fig.add_subplot(2,3,5) # 2 rows, 3 columns, 5th position
    axes_4 = fig.add_subplot(2,3,6) # 2 rows, 3 columns, 6th position

    # Defining axes_1 plot
    axes_1.plot(df[col_no_smooth], "b", linewidth = 2)
    axes_1.plot(df[col_smooth_7_days], "g", linewidth = 2)
    axes_1.plot(df[col_smooth_30_days], "r", linewidth = 2)
    axes_1.set_title("Daily mean sentiment score of headlines \n and smoothing differences")
    axes_1.set_xlabel(f"Days after {start_date}")
    axes_1.set_ylabel("Mean sentiment scores")
    
    # Defining axes_2 plot
    axes_2.set_title("Daily mean sentiment score of headlines")
    axes_2.set_ylabel("Mean sentiment score")
    axes_2.set_xlabel(f"Days after {start_date}")
    axes_2.plot(df[col_no_smooth], "b", linewidth = 2)
    axes_2.legend("Daily", loc="upper left")

    # Defining axes_3 plot
    axes_3.set_title("Daily mean sentiment score of headlines \n (smoothed, 7-day window)")
    axes_3.set_ylabel("Mean sentiment score (smoothed, 7-days)")
    axes_3.set_xlabel(f"Days after {start_date}")
    axes_3.plot(df[col_smooth_7_days], "g", linewidth = 2)
    axes_3.legend("Weekly average around the date", loc="upper left")

    # Defining axes_4 plot
    axes_4.set_title("Daily mean sentiment score of headlines \n (smoothed, 30-day window")
    axes_4.set_ylabel("Mean sentiment score (smoothed, 30-days)")
    axes_4.set_xlabel(f"Days after {start_date}")
    axes_4.plot(df[col_smooth_30_days], "r", linewidth = 2)
    axes_4.legend("Monthly average around the date", loc="upper left")

    # So that the font doesn't overlap
    plt.tight_layout()
    
    # To save
    if save == True:
        plt.savefig("sentiment_polarity_plot.png")

    # To show the plot
    # plt.show(fig)




if __name__=="__main__":
    convert_to_datetime(df, "publish_date")
    calc_sentiment(df, "headline_text")
    df_dates = calc_daily_avg_sentiment(df, "publish_date", "sentiment_score")
    plot_sentiment(df = df_dates, 
    start_date = "2003-02-19",
    col_no_smooth = "daily_mean_polarity_score",
    col_smooth_7_days = "daily_polarity_score_weekly_smooth",
    col_smooth_30_days = "daily_polarity_score_monthly_smooth", save = True)
