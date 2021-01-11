import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from hackpion.EyHelper import (get_all_hashtags , get_all_mentions ,strip_all_entities ,sentiment_final , sentiment_final_int,
                        sentiment_analyzer_scores_text_blob)
import dash_bootstrap_components as dbc
import dash_html_components as html
def preprocessData(df):
    df["mentions"] = df.tweet.apply(lambda x: get_all_mentions( str(x)))
    df["hashtags"] = df.tweet.apply(lambda x: get_all_hashtags( str(x)))
    df["cleaned_review"] = df.tweet.apply(lambda x: strip_all_entities(str(x).lower()))
    df["sentiment_polarity"] = df.cleaned_review.apply(sentiment_analyzer_scores_text_blob)
    df["sentiment"] = df.sentiment_polarity.apply(sentiment_final)
    df["sentiment_int"] = df.sentiment_polarity.apply(sentiment_final_int)
    return df

def update_sentiment_trend(selected_options , timeframe):
    with open('database/compet_database.json', 'r') as openfile: 
            data = json.load(openfile) 
    comp = pd.DataFrame(data['username'])
    competitors = comp.loc[comp.compet].screen_name.values
    self_account = comp.loc[~comp.compet].screen_name.values
    search_base = [{comp_:[comp_]} for comp_ in competitors]+[{"EY":list(self_account)}]
        
    ey = pd.DataFrame()
    for i in self_account:
        ey = pd.concat([ey,pd.read_csv('database/userdata/{}_user_profile.csv'.format(i))])

    compet = pd.DataFrame()
    for i in competitors:
        compet = pd.concat([compet,pd.read_csv('database/userdata/{}_user_profile.csv'.format(i))])
    

    print(selected_options,timeframe)
    ey['Week'] = pd.to_datetime(ey['date']).dt.strftime('%U')
    ey['month'] =ey.date.apply(lambda x: x[:7])
    like_ey_pos =ey.loc[ey.sentiment_int==1].groupby(by=timeframe).sentiment_int.count().reset_index()
    like_ey_pos['Type'] = "Positive Sentiment"
    like_ey_neg =ey.loc[ey.sentiment_int==-1].groupby(by=timeframe).sentiment_int.count().reset_index()
    like_ey_neg['Type'] = "Negative Sentiment"

    like_ =ey.groupby(by=timeframe).likes_count.mean().reset_index()
    like_['Type'] = "Likes Count"
    like_.columns= like_ey_neg.columns
    like_ey =ey.groupby(by=timeframe).sentiment_int.count().reset_index()
    like_ey['Type'] = "All Tweets"

    avg = like_.copy()
    avg.sentiment_int=like_.sentiment_int.mean()
    avg.Type="Mean"
    count_data = pd.concat([like_ey ,like_ey_neg , like_ey_pos,like_])
    count_data = count_data.loc[count_data.Type.isin(selected_options)]
    fig_line_all = px.line(count_data, x=timeframe, y="sentiment_int",color="Type",title="Trend for tweets")
    fig_line_all.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    
    plot_bgcolor='white'
)   
    return fig_line_all

def sentiment_distribution_chart():
    with open('database/compet_database.json', 'r') as openfile: 
            data = json.load(openfile) 
    comp = pd.DataFrame(data['username'])
    competitors = comp.loc[comp.compet].screen_name.values
    self_account = comp.loc[~comp.compet].screen_name.values
    search_base = [{comp_:[comp_]} for comp_ in competitors]+[{"EY":list(self_account)}]
        
    ey = pd.DataFrame()
    for i in self_account:
        ey = pd.concat([ey,pd.read_csv('database/userdata/{}_user_profile.csv'.format(i))])

    compet = pd.DataFrame()
    for i in competitors:
        compet = pd.concat([compet,pd.read_csv('database/userdata/{}_user_profile.csv'.format(i))])
        

    fig = make_subplots(rows=1, cols=2, start_cell="bottom-left",subplot_titles = ["EY" ,"Competitor"])
    
    fig.add_trace(go.Bar(x= ey.sentiment.value_counts().index,y= ey.sentiment.value_counts().values,name="EY"),
                  row=1, col=1)

    fig.add_trace(go.Bar(x= compet.sentiment.value_counts().index,y= compet.sentiment.value_counts().values,name="Competitor"),
                  row=1, col=2)

    fig.update_layout( plot_bgcolor='white')
    return fig


def prepeare_Sentiment_content(dashboard):
    with open('database/compet_database.json', 'r') as openfile: 
            data = json.load(openfile) 
    comp = pd.DataFrame(data['username'])
    competitors = comp.loc[comp.compet].screen_name.values
    self_account = comp.loc[~comp.compet].screen_name.values
    search_base = [{comp_:[comp_]} for comp_ in competitors]+[{"EY":list(self_account)}]
        
    ey = pd.DataFrame()
    for i in self_account:
        ey = pd.concat([ey,pd.read_csv('database/userdata/{}_user_profile.csv'.format(i))])

    compet = pd.DataFrame()
    for i in competitors:
        compet = pd.concat([compet,pd.read_csv('database/userdata/{}_user_profile.csv'.format(i))])
        




 

    alert = dbc.Alert(
        [
            html.P("Sentiment Analysis helps nderstand how our users feel about a topic or your brand and compare it with other competitors."),
            html.P("Time Period: Choose a timeline for which you want the analysis"),
            html.P("Line chart representation of the sentiment spread of  in different timeframes "),
            html.P("Donut chart to represent different languages used in the tweets")
        ]
    )

    multiselect = html.Div(children = [dcc.Dropdown(id='multi_select_option',
                                       options=[
                                            {'label': 'All Tweets', 'value': 'All Tweets'},
                                            {'label': 'Negative Sentiment', 'value': 'Negative Sentiment'},
                                            {'label': 'Positive Sentiment', 'value': 'Positive Sentiment'}
                                        ],
                                        value=['All Tweets'],

                                        multi=True
                                    )],style={'display': 'inline-block' , 
                                              "width" :"60%",
                                              "padding-left":"70px",
                                              "padding-right":"50px"})

    radio_button = dcc.RadioItems(id='timeframe_selection',
            options=[
                {'label': 'Daily', 'value': 'date'},
                {'label': 'Weekly', 'value': 'Week'},
                {'label': 'Monthly', 'value': 'month'}
            ],
        style={'display': 'inline-block'},

            value='Week'
        )
    
    
    date_range = dcc.DatePickerRange(
    start_date_placeholder_text="Start Period",
    end_date_placeholder_text="End Period",
    calendar_orientation='vertical')  


    selectors= html.Div(children = [date_range , html.Div([multiselect , radio_button])],style={'display': 'flex','justify-content':'space-around'})
    
    sentiment_content_up = html.Div(children =[dcc.Graph(id='sentiment_comparison',
                                                      figure=sentiment_distribution_chart(),
                                                      style={'width': '75vh', 'height': '55vh','display': 'inline-block',
                                                             "box-shadow":"0 8px 16px 0 rgba(0,0,0,0.2)"}),

                                            dcc.Graph(id='example-graph_2',
                                                      style={'width': '75vh', 'height': '55vh','display': 'inline-block',
                                                             "box-shadow":"0 8px 16px 0 rgba(0,0,0,0.2)"})],
                                 style={'display': 'flex','justify-content':'space-between','width':'90%','margin':"auto"})


    colors = [ 'lightgreen', 'mediumturquoise', 'darkorange' ]

    fig_language = go.Figure(data=[go.Pie(labels=["English" ,"French" , "Hindi" ],
                                 values=[80,15,5],hole=0.4 ,title="Language Distribution")])
    
    fig_language.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))

    
    
    
    sentiment_content_down = html.Div(children =[
                                        dcc.Graph(figure=fig_language,id='language_graph',
                                                  style={'width': '75vh', 'height': '55vh','display': 'inline-block',
                                                         "box-shadow":"0 8px 16px 0 rgba(0,0,0,0.2)"})
                                                ],
                             style={'display': 'flex','justify-content':'space-between','width':'90%','margin':"auto","padding-top":"10px"})


    page_sentiment_content = html.Div(children = [ dashboard ,alert , selectors , html.Div([sentiment_content_up, sentiment_content_down],style={'padding':"30px"})],style={'padding':"30px"})

    
    
    return page_sentiment_content


companies_present = {"ey":"Ey", "pwc":"PWC"  , "kpmg":"KPMG" , "deliotte":"Deliotte"}
colors = {'Negative': 'red',
          'Neutral': 'blue',
          'Positive': 'lightgreen'}
        ######## reading data ########

