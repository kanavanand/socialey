import os
import twint
import pandas as pd
from .EyHelper import (get_all_hashtags , get_all_mentions ,strip_all_entities ,sentiment_final , sentiment_final_int,
                        sentiment_analyzer_scores_text_blob)


dataColumns = ["id","username","date","time","tweet","user_id","timezone","mentions","hashtags","replies_count","likes_count",'retweets_count','replies_count']


def preprocessData(filePath):
    df = pd.read_csv(filePath)
    df["mentions"] = df.tweet.apply(lambda x: get_all_mentions( str(x)))
    df["hashtags"] = df.tweet.apply(lambda x: get_all_hashtags( str(x)))
    df["cleaned_review"] = df.tweet.apply(lambda x: strip_all_entities(str(x).lower()))
    df["sentiment_polarity"] = df.cleaned_review.apply(sentiment_analyzer_scores_text_blob)
    df["sentiment"] = df.sentiment_polarity.apply(sentiment_final)
    df["sentiment_int"] = df.sentiment_polarity.apply(sentiment_final_int)
    df.to_csv(filePath,index=None)

    

def getUserNameData(user_name,date_start = '2018-01-01',date_end='2020-11-01'):
    filePath = "userdata/{}_user_profile.csv".format(user_name)
    if os.path.exists(filePath):
        print("File with same name is already there,  removing it... ")
        os.remove(filePath)
    c = twint.Config()
    c.Username = user_name
    c.Custom["tweet"] = ["id"]
    c.Custom["user"] = ["bio"]
    c.Since = date_start
    c.Until = date_end
    c.Store_pandas=True
    c.Stats= True
    c.Custom["tweet"]=dataColumns
    c.Hide_output = True
    c.Store_csv = True
    c.Output = filePath
    twint.run.Search(c)
    preprocessData(filePath)
    print("Data scraping completed")
    
def getSearchResult(query , date_start = '2018-01-01',date_end='2020-11-01'):
    filePath = "{}_query.csv".format(query)
    if os.path.exists(filePath):
        print("File with same name is already there,  removing it... ")
        os.remove(filePath)
    c = twint.Config()
    c.Search = query
    c.Custom["tweet"] = ["id"]
    c.Custom["user"] = ["bio"]
    c.Since = date_start
    c.Until = date_end
    c.Store_pandas=True
    c.Stats= True
    c.Custom["tweet"]=dataColumns
    c.Hide_output = True
    c.Store_csv = True
    c.Output = filePath
    twint.run.Search(c)
    preprocessData(filePath)
    print("Data scraping completed")
    
  