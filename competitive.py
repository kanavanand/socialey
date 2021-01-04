from sentiment import preprocessData
import itertools
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
img_url = "https://www.ntaskmanager.com/wp-content/uploads/2020/01/Sentiment-Analysis.png"
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc
import pandas as pd


kpmg = preprocessData(pd.read_csv('data/KPMG.csv'))
ey = preprocessData(pd.read_csv('data/ey_news.csv'))
deliotte = preprocessData(pd.read_csv('data/Deloitte.csv'))
pwc = preprocessData(pd.read_csv('data/pwc.csv'))
data_dic = {"ey":ey, "pwc":pwc  , "kpmg":kpmg , "deliotte":deliotte}


def top_n_trending_hash_month(hashtags , number):
    all_hashtags = list(itertools.chain.from_iterable(hashtags))
    hashtags = pd.Series(all_hashtags).apply(lambda x: x.lower()).value_counts().head(number)
    return hashtags

def top_n_trending_hash_month_df(data,number=10):
    data["mentions"] = data.tweet.apply( lambda x: get_all_mentions( str(x) )  )
    data["hashtags"] = data.tweet.apply( lambda x: get_all_hashtags( str(x) )  )
    data['month'] =data.date.apply(lambda x: x[:7])

    data.hashtags = data.hashtags.apply(lambda x: [i.lower() for i in x])
    hdf = data.groupby(by='month').hashtags.apply(lambda x: top_n_trending_hash_month(x , number)).reset_index()
    hdf.columns =['Month','Hashtags','Frequency']
    return hdf


def give_company_comparison(dashboard,company = "kpmg"):
    s= pd.DataFrame(top_n_trending_hash_month(data_dic[company].hashtags,-1))

    s['ey']=top_n_trending_hash_month(ey.hashtags,-1)
    s.columns=['kpmg','ey']

    a=s.loc[s.ey.notnull()].sort_values(by="ey")
    a['diff'] =a.ey-a.kpmg

    a.sort_values(by="diff").head(20)


    tb = a.sort_values(by="diff",ascending=False).head(20)['diff'].reset_index()
    tb.columns= ['Topic' , 'Ahead By']
    tb.head()

    lb = a.sort_values(by="diff",ascending=True).head(20)['diff'].reset_index()
    lb.columns= ['Topic' , 'Lagging By']
    lb.head()
    
    dropdown = html.Div([dcc.Dropdown(
    id='xaxis-column',
    options=[{'label': i, 'value': i} for i in ["EY" ]],
    value="EY",
    style={"width":"30vh" }
    ),
        html.H3("V/S"),


    dcc.Dropdown(
        id='xaxis-column_2',
        options=[{'label': i, 'value': i} for i in [ "KPMG" , "PWC" , "Deliotte"]],
        value="KPMG",style={"width":"30vh" })],style={'display': 'flex','justify-content':'space-between','width':'46%','margin':"auto","padding":"30px"})




    table1 = html.Div([html.H2(" Leading Topics ",style={"font-size":"3rem","display":"flex","justify-content":"space-around","padding-bottom":"2pc"}) , 
                       dbc.Table.from_dataframe(tb, striped=True, bordered=True, hover=True)],
                    style ={'width': '75vh','display': 'inline-block',"margin":"47px"} )

    table2 = html.Div([html.H2(" Lagging Topics ",style={"font-size":"3rem","display":"flex","justify-content":"space-around","padding-bottom":"2pc"}) , 
                       dbc.Table.from_dataframe(lb, striped=True, bordered=True, hover=True , dark=True)],
                    style ={'width': '75vh','display': 'inline-block',"margin":"47px"} )

    table= html.Div(id="table_area_compet",style = {'display': 'flex','justify-content':'space-between','width':'90%','margin':"auto"} )
    return html.Div([dashboard,dropdown , table ])
def give_company_comparison_2(company = "kpmg"):
    s= pd.DataFrame(top_n_trending_hash_month(data_dic[company].hashtags,-1))

    s['ey']=top_n_trending_hash_month(ey.hashtags,-1)
    s.columns=['kpmg','ey']

    a=s.loc[s.ey.notnull()].sort_values(by="ey")
    a['diff'] =a.ey-a.kpmg

    a.sort_values(by="diff").head(20)


    tb = a.sort_values(by="diff",ascending=False).head(20)['diff'].reset_index()
    tb.columns= ['Topic' , 'Ahead By']
    tb.head()

    lb = a.sort_values(by="diff",ascending=True).head(20)['diff'].reset_index()
    lb.columns= ['Topic' , 'Lagging By']
    lb.head()
    


    table1 = html.Div([html.H2(" Leading Topics ",style={"font-size":"3rem","display":"flex","justify-content":"space-around","padding-bottom":"2pc"}) , 
                       dbc.Table.from_dataframe(tb, striped=True, bordered=True, hover=True)],
                    style ={'width': '75vh','display': 'inline-block',"margin":"47px"} )

    table2 = html.Div([html.H2(" Lagging Topics ",style={"font-size":"3rem","display":"flex","justify-content":"space-around","padding-bottom":"2pc"}) , 
                       dbc.Table.from_dataframe(lb, striped=True, bordered=True, hover=True , dark=True)],
                    style ={'width': '75vh','display': 'inline-block',"margin":"47px"} )

    return [table1,table2]

