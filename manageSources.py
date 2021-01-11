from twitter import *
import json
import os
import numpy as np
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
from hackpion.EyMiner import getUserNameData,getSearchResult
import dash
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import pandas as pd
import json


consumer_key= "5Q2KlNFSYIDmPQHOYWFEPKV9y"
consumer_secret = "AJ2hGakUkbvu1l5ljkCorkDRfdc3nvShsTTZVWcMrSuyjS2bwb"
access_token = "3247480256-GUxZFRMvhZryuXCaQGaFXiQwuEmnOX6nsV1Wjri"
access_token_secret= "9ljCN8VSir43hRg1AQ5KDARwDPo7oHswMAmoUJblc8xsX"
bearer_token = "AAAAAAAAAAAAAAAAAAAAACr0JwEAAAAAk0NGdSY6XfsIe7OudbsorkqZ0DU%3Dh1ZJ4SnRfNiom7FVDPIpfpY4I3fgTxeHLQJe0xYFwp683PGAma"

twitter = Twitter(auth = OAuth( access_token,
                  access_token_secret,consumer_key,
                  consumer_secret))

def searchUserKeyword(keyword,compet=False):
    '''
    update the search results in dropdown list for username search
    '''
    print("Seaching for  keyword",keyword)
    results = twitter.users.search(q = keyword)
    userDropdownList = []
    for user in results:
        user['compet']=compet
        userDropdown={}
        userDropdown['label'] = user["screen_name"]
        userDropdown['value'] = user["screen_name"]
        userDropdown['data']  = dict((k, user[k]) for k in ('name', 'screen_name', 'location' ,'followers_count','profile_image_url','compet'))
        userDropdownList.append(userDropdown)
    return userDropdownList


def updateSearchDataBase(search):
    '''
    Update the search database displayed on the manage sources page
    '''
    if search:
            with open('database/search_database.json', 'r') as openfile: 
                data = json.load(openfile) 
            openfile.close()
            if not any([Search for Search in data['search'] if Search['query']==search]):
                print("In updateSearchDataBase for word: ",search)
                userdata = getSearchResult(search)
                userdata['query']=search
                data['search'].append(userdata)
                print("rows scraped:",userdata['count'])
                with open('database/search_database.json', 'w') as f:
                    json.dump(data, f)
                f.close()
def updateCompetDataBase(username,compet=False):
    '''
    Update the USER database displayed on the manage sources page
    '''
    if username:
            with open('database/compet_database.json', 'r') as openfile: 
                data = json.load(openfile) 
            openfile.close()
            if not any([user for user in data['username'] if user['screen_name']==username]):
                results = searchUserKeyword(username,compet)
                for i in results:
                    if i['label']==username:
                        userdata = i['data']
                        break
                print("The username going for scrape",username)
                getUserNameData(username)
                data['username'].append(userdata)
                with open('database/compet_database.json', 'w') as f:
                    json.dump(data, f)
                f.close()
def generate_table(df, max_rows=10):
    """
    Print generating new table
    """
    with open('database/search_database.json', 'r') as openfile: 
            search_database = json.load(openfile) 

    tool_tip_data = [{'Tracking Entity':{'type': 'markdown','value':create_tabluated_data(ent['query'])}} for ent in search_database['search']]
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
    tooltip_data=tool_tip_data,tooltip_duration=None,
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
        style_table={'height': '100vh', 'overflowY': 'auto'} )


def searchbaseTable():
    print("In Search Base Table")
    with open('database/search_database.json', 'r') as openfile: 
        data = json.load(openfile) 
    data = pd.DataFrame(data['search'])
    data.columns = ['Total Tweet Count' , 'Positive Sentiment Count' , 'Negative Sentiment Count' , 'Tracking Entity']
    tb = data[['Tracking Entity','Total Tweet Count' , 'Positive Sentiment Count' , 'Negative Sentiment Count']]
    table_ = generate_table(tb)
    print("Displaying the content from searchbasetable")
    return    html.Div([table_])



def makeCard(smp):
    card = html.Div(children=[dbc.Card(
        [
            dbc.CardImg(src=smp["profile_image_url"], top=True,style={'height':"50px",'width':'50px'}),
            dbc.CardBody(
                [
                    html.H6(smp['screen_name'], className="card-title"),
                    html.P("Followers:"),
                    html.P(smp["followers_count"]),
                ]
            )
        ]
    ,style={'padding':"10px 10px 0px 10px"})],style={'padding':"15px"})
    return card


def create_tabluated_data(query):
        tweets = pd.read_csv("database/searchdata/{}_query.csv".format(query))['tweet']
        with open('database/compet_database.json', 'r') as openfile: 
            data = json.load(openfile) 
        comp = pd.DataFrame(data['username'])
        competitors = comp.loc[comp.compet].screen_name.values
        self_account = comp.loc[~comp.compet].screen_name.values
        search_base = [{comp_:[comp_]} for comp_ in competitors]+[{"EY":list(self_account)}]
        leader_board = pd.DataFrame([{ "Company": list(ent.keys())[0], "Count":sum(tweets.apply(lambda x: any([e for e in ent if e.lower() in x.lower()]))) }for ent in search_base ])
        leader_board = leader_board.sort_values(by='Count',ascending = False)
        leader_board['Rank']= np.arange(1,leader_board.shape[0]+1)
        leader_board = leader_board[['Rank' , 'Company', 'Count']]
        return leader_board.set_index('Rank').to_markdown()
    

def prepeare_ManageSources_content(dashboard):
    alert = dbc.Alert(
        [
            html.P("1. Manage Sources acts as a settings page for SocialEy where you can select choices for analysis and it remains static for a user."),
            html.P("2. EY handles: On the Left most, this search bar is for adding different EY handles "),
            html.P("3.Competitors handles: Add as many competitors handle you want to compare"),
            html.P("4. Search Hashtags: Any topic or hashtags you want statistics ad performace about will come here Hovering on the hashtag, gives you the positioning of Big4 in terms of their activeness for the particular hashtag."),
            ]
    )

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css",dbc.themes.BOOTSTRAP]
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    ey_cards = html.Div(id="ey_cards",style={'display':"flex","overflow":"scroll"})
    comp_cards = html.Div(id="comp_cards",style={'display':"flex","overflow":"scroll"})


    left_side_ey    = html.Div(id="left_side",children=[html.H2("EY Handles",style={"background-color": "ghostwhite",
        "padding": "16px",
        "display": "flex",
        'justify-content': "center",
        "font-size": "27px",
        "font-family": 'ui-serif'}),html.Div(children = [dcc.Dropdown(id="my-dynamic-dropdown",style={"width":"100%"}),
                                                     html.Button('Submit', id='submit-val',n_clicks=0)],style={'display':"flex",'padding-left':"88px"}),
                                                     html.Div(id='container-button-basic',children='Enter a value and press submit'),ey_cards],
                                   style={'width':"48%",'background-color':'rgb(231, 250, 207)'})


    right_side_comp = html.Div(id="right_side",children = [html.H2("Competitors Handles" ,style={"background-color": "ghostwhite",
        "padding": "16px",
        "display": "flex",
        'justify-content': "center",
        "font-size": "27px",
        "font-family": 'ui-serif'}) , html.Div(children = [dcc.Dropdown(id="comp-dynamic-dropdown",style={"width":"100%"}),
                                                                                html.Button('Submit', id='submit-val-comp',n_clicks=0)],style={'display':"flex",'padding-left':"88px"}),
                                                          html.Div(id='container-button-basic-comp',children='Enter a value and press submit'),comp_cards],
                               style={'width':"48%",'background-color':'rgb(255, 214, 222)'})



    hashtag_layout = html.Div(children = [html.H2("Search Hashtags",style={"background-color": "ghostwhite",
        "padding": "16px",
        "display": "flex",
        'justify-content': "center",
        "font-size": "27px",
        "font-family": 'ui-serif'}),
                                          html.Div(id="hash_search_",children = [dcc.Input(id="search_hashtag",placeholder="Input hashtag you want to track",style={'width':"41%"}),
                                          html.Button("Submit", id='submit_hashtag',n_clicks=0)],style={  "display": "flex",
                                                                                                            "justify-content": "center",
                                                                                                            "padding": "26px"}),
                                          html.Div(id='search_table_2')])


    manage_sources_page_content = html.Div(children = [html.Div(id="ey_comp" , children = [left_side_ey,right_side_comp],style={"display":"flex",'justify-content':'space-between'}),hashtag_layout])
    app.layout = html.Div(manage_sources_page_content)
    manage_sources = html.Div(children = [dashboard,alert , manage_sources_page_content])
    return manage_sources

        
        
