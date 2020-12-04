import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

companies_present = {"ey":"Ey", "pwc":"PWC"  , "kpmg":"KPMG" , "deliotte":"Deliotte"}

#### remove this dependen..
from .EyHelper import (get_all_hashtags , get_all_mentions ,strip_all_entities ,sentiment_final , sentiment_final_int,
                        sentiment_analyzer_scores_text_blob)

def preprocessData(df):
    df["mentions"] = df.tweet.apply(lambda x: get_all_mentions( str(x)))
    df["hashtags"] = df.tweet.apply(lambda x: get_all_hashtags( str(x)))
    df["cleaned_review"] = df.tweet.apply(lambda x: strip_all_entities(str(x).lower()))
    df["sentiment_polarity"] = df.cleaned_review.apply(sentiment_analyzer_scores_text_blob)
    df["sentiment"] = df.sentiment_polarity.apply(sentiment_final)
    df["sentiment_int"] = df.sentiment_polarity.apply(sentiment_final_int)
    return df

    
kpmg = preprocessData(pd.read_csv('data/KPMG.csv'))
ey = preprocessData(pd.read_csv('data/ey_news.csv'))
deliotte = preprocessData(pd.read_csv('data/Deloitte.csv'))
pwc = preprocessData(pd.read_csv('data/pwc.csv'))
data_dic = {"ey":ey, "pwc":pwc  , "kpmg":kpmg , "deliotte":deliotte}

def show_sentiment_plot(company="ey"):
    df = data_dic[company]
    sns.countplot(x='sentiment',data=df)
