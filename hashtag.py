import dash_bootstrap_components as dbc
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import os
import pandas as pd
import dash_table
img_url = "https://www.ntaskmanager.com/wp-content/uploads/2020/01/Sentiment-Analysis.png"
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from sentiment import preprocessData
import dash_html_components as html
standard_Style = {'width': '75vh', 'height': '45vh','display': 'inline-block'}
import pandas as pd
def makeCardContent(header,title):
    card_content = [
        dbc.CardHeader(header),
        dbc.CardBody(
            [
                html.H2(title, className="card-title")
                
            ]
        ),
    ]
    return card_content

def makeCard(data):
    data.fillna(0,inplace=True)
    dc = {
        "Total Tweets":data.shape[0],
        "Average Sentiment":str(data.sentiment_int.mean())[:4],
        "Average Likes": str(data.likes_count.mean())[:4],
        "Total Comments":str(data['replies_count.1'].sum())
    }
    row_1 = dbc.Row(
        [
            dbc.Col(dbc.Card(makeCardContent("Total Tweets",dc["Total Tweets"]), color="secondary", outline=True)),
            dbc.Col(dbc.Card(makeCardContent("Average Sentiment",dc["Average Sentiment"]), color="secondary", outline=True)),
        ],
        className="mb-4",
    )

    row_2 = dbc.Row(
        [
            dbc.Col(dbc.Card(makeCardContent("Average Likes" , dc["Average Likes"]), color="secondary", outline=True)),
            dbc.Col(dbc.Card(makeCardContent("Total Comments",dc["Total Comments"]) , color="secondary", outline=True)),
        ],
        className="mb-4",
    )


    cards = html.Div([row_1, row_2],style={'width': '75vh', 'display': 'inline-block',
                                                             "box-shadow":"0 8px 16px 0 rgba(0,0,0,0.2)","padding":"20px"})
    return cards

from hackpion.EyMiner import getUserNameData,getSearchResult
from datetime import datetime,timedelta
def get_data_for_campaign(hashTag):
    print("scapring ",hashTag)
    hashTag = hashTag.lower()
    end_date = datetime.strftime(datetime.today(),'%Y-%m-%d')
    start_date = datetime.strftime(datetime.today()-timedelta(days=4),'%Y-%m-%d')
    getSearchResult(hashTag,start_date,end_date)
    return pd.read_csv("{}_query.csv".format(hashTag))



import numpy as np


def generate_table(df, max_rows=10):
    df = df[['date','tweet','sentiment']].head(10)
    return dash_table.DataTable(
    style_data={
        'whiteSpace': 'normal',
    },
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    css=[{
        'selector': '.dash-spreadsheet td div',
        'rule': '''
            display: block;
        '''
    }],
    tooltip_data=[
        {
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        } for row in df.to_dict('rows')
    ],
    tooltip_duration=None,

    style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'font_size': '20px',
            'text_align': 'center',
            'maxWidth': '500px'
        },
                style_cell_conditional=[{
            'if': {'column_id': c},
            'textAlign': 'left'} for c in ['date', 'tweet']],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_table={'height': '32vh', 'overflowY': 'auto'}

        
        
        
)

def hashtag_graphs(hashTag='#BetterWorkingWorld',pain_point=[]):
    filePath = "{}_query.csv".format(hashTag.lower())
    if os.path.exists(filePath):
        data = pd.read_csv(filePath)
    else:
        data = get_data_for_campaign(hashTag)
#     data = preprocessData(pd.read_pickle('../supply_chain1.pkl'))
    pain_points= [' hit ','suffer','poor','bad','not good','affected','problem']
    if len(pain_point)>0:
        data = data.loc[data.tweet.apply(lambda x: any([i for i in pain_points if i in x.lower()]))].sort_values('likes_count',ascending=False)

#     data = pd.read_csv('#betterworkingworld_query.csv')
    best_users = pd.DataFrame(data.username.value_counts().head(10)).reset_index()
    fig = px.bar(best_users, y='username', x='index', text='username')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(
       

        plot_bgcolor='white'
    )
    date_ = data.date.value_counts().sort_index().reset_index()
    fig2 = px.line(date_, x="index", y="date", title='Trend for this month for hashtag')
    fig2.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),

        plot_bgcolor='white'
    )
    cards = makeCard(data)
    table = generate_table(data)
    return fig,fig2,cards,table
                  
                  
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

def prepeare_Hashtag_content(dashboard): 
    switches = dbc.FormGroup(
    [
#         dbc.Label("Toggle a bunch"),
        dbc.Checklist(
            options=[
                {"label": "Pain Points", "value": 1},
            ],
            value=[],
            id="switches-input",
            switch=True,
            inputStyle={'font-size':"30px",'zoom':1.6},
            labelStyle={'font-size':"20px"},
            labelCheckedStyle={"color": "red",'font-size':"20px"},
        ),
    ]
)

    text_input = html.Div(
        [
            dbc.Input(id="input-1-state", placeholder="Type something...", type="text"),
            html.Br(),
        ]
    )


    Input_feilds = html.Div([
        dbc.Input(id="input-1-state", placeholder="Type something... default(#ey)", type="text",value="#ey",style={'width':"70%",'padding-bottom':"20px"}),
        switches,
        dbc.Button("Submit", id='submit-button-state', n_clicks=0, color="primary", className="mr-1"),
        html.Div(id='output-state', style={'whiteSpace': 'pre-line'})
    ],style={"padding":"19px",'justify-content':"space-between",'display':"flex",'margin':"auto",'width':"45%"})

    page_buzzwords_content = html.Div([dashboard , Input_feilds  ,html.Div(id="hashtag_full") ])    
    return page_buzzwords_content
                  
                  
                  
