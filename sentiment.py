import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from hackpion.EyHelper import (get_all_hashtags , get_all_mentions ,strip_all_entities ,sentiment_final , sentiment_final_int,
                        sentiment_analyzer_scores_text_blob)



def preprocessData(df):
    df["mentions"] = df.tweet.apply(lambda x: get_all_mentions( str(x)))
    df["hashtags"] = df.tweet.apply(lambda x: get_all_hashtags( str(x)))
    df["cleaned_review"] = df.tweet.apply(lambda x: strip_all_entities(str(x).lower()))
    df["sentiment_polarity"] = df.cleaned_review.apply(sentiment_analyzer_scores_text_blob)
    df["sentiment"] = df.sentiment_polarity.apply(sentiment_final)
    df["sentiment_int"] = df.sentiment_polarity.apply(sentiment_final_int)
    return df



def update_sentiment_trend(selected_options , timeframe):
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
    fig_line_all = px.line(count_data, x=timeframe, y="sentiment_int",color="Type")
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
    fig = make_subplots(rows=2, cols=2, start_cell="bottom-left")

    fig.add_trace(go.Bar(x= ey.sentiment.value_counts().index,y= ey.sentiment.value_counts().values,name="EY"),
                  row=1, col=1)

    fig.add_trace(go.Bar(x= kpmg.sentiment.value_counts().index,y= kpmg.sentiment.value_counts().values,name="KPMG"),
                  row=1, col=2)

    fig.add_trace(go.Bar(x= pwc.sentiment.value_counts().index,y= pwc.sentiment.value_counts().values,name="PWC"),
                  row=2, col=1)

    fig.add_trace(go.Bar(x= deliotte.sentiment.value_counts().index,y= deliotte.sentiment.value_counts().values,name="Deliotte"),
                  row=2, col=2)

    fig.update_layout( plot_bgcolor='white')
    return fig


def prepeare_Sentiment_content(dashboard):

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


    page_sentiment_content = html.Div(children = [ dashboard , selectors , html.Div([sentiment_content_up, sentiment_content_down],style={'padding':"30px"})],style={'padding':"30px"})

    
    
    return page_sentiment_content


companies_present = {"ey":"Ey", "pwc":"PWC"  , "kpmg":"KPMG" , "deliotte":"Deliotte"}
colors = {'Negative': 'red',
          'Neutral': 'blue',
          'Positive': 'lightgreen'}
        ######## reading data ########

kpmg = preprocessData(pd.read_csv('data/KPMG.csv'))
ey = preprocessData(pd.read_csv('data/ey_news.csv'))
deliotte = preprocessData(pd.read_csv('data/Deloitte.csv'))
pwc = preprocessData(pd.read_csv('data/pwc.csv'))
data_dic = {"ey":ey, "pwc":pwc  , "kpmg":kpmg , "deliotte":deliotte}
