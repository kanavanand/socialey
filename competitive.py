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
import json
import ast 
import numpy as np

def  tabulatedToolData(dataCombined , hashtag_):
    data_combined = dataCombined.loc[dataCombined.hashtags.apply(lambda x: any([i for i in x if hashtag_ == i.lower()]))]
    leaderBoard= data_combined.groupby(by='Company').hashtags.count().sort_values(ascending=False).reset_index()
    leaderBoard['Rank']= np.arange(1,leaderBoard.shape[0]+1)
    leaderBoard.columns = ['Company', 'Count','Rank' ]
    leaderBoard = leaderBoard[['Rank' , 'Company', 'Count']]
    return leaderBoard.set_index('Rank').to_markdown()


def generate_table(df, max_rows=10):
    with open('database/compet_database.json', 'r') as openfile: 
            data = json.load(openfile) 
    comp = pd.DataFrame(data['username'])
    competitors = comp.loc[comp.compet].screen_name.values
    self_account = comp.loc[~comp.compet].screen_name.values
    search_base = [{comp_:[comp_]} for comp_ in competitors]+[{"EY":list(self_account)}]


    ey = pd.DataFrame()
    for i in self_account:
        ey = pd.concat([ey,pd.read_csv('database/userdata/{}_user_profile.csv'.format(i))])
    ey['Company'] = "EY"
    compet = pd.DataFrame()
    for i in competitors:
        tmp=pd.read_csv('database/userdata/{}_user_profile.csv'.format(i))
        tmp['Company']=i
        compet = pd.concat([compet,tmp])
    data_combined = pd.concat([ey , compet]) 
    data_combined.hashtags = data_combined.hashtags.apply(ast.literal_eval)


    """
    Print generating new table
    """
#     with open('database/search_database.json', 'r') as openfile: 
#             search_database = json.load(openfile) 
    
    tool_tip_data = [{'Topic':{'type': 'markdown','value':tabulatedToolData(data_combined,  ent)}} for ent in df.Topic.values]
    
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




def give_company_comparison(dashboard,company = "KPMG"):
    

    alert = dbc.Alert(
        [
            html.P("Competitor’s Analysis helps evaluate your competitor’s strategies and weaknesses."),
            html.P("EY vs your choosen competitor. Gives you leading and lagging topics for them."),
            html.P("Don't forget to hover over these topics to get brand positioning among BIg4."),
        ]
    )


    with open('database/compet_database.json', 'r') as openfile: 
                data = json.load(openfile) 
    comp = pd.DataFrame(data['username'])
    competitors = comp.loc[comp.compet].screen_name.values
    self_account = comp.loc[~comp.compet].screen_name.values
    search_base = [{comp_:[comp_]} for comp_ in competitors]+[{"EY":list(self_account)}]

    ey = pd.DataFrame()
    for i in self_account:
        ey = pd.concat([ey,pd.read_csv('database/userdata/{}_user_profile.csv'.format(i))])
    
    
    data_frame = pd.read_csv('database/userdata/{}_user_profile.csv'.format(company))
    import ast 
    ey.hashtags = ey.hashtags.apply(ast.literal_eval)
    data_frame.hashtags = data_frame.hashtags.apply(ast.literal_eval)
    print("COMPET ARE LOADED",competitors)
    print('*'*77)
    
    s= pd.DataFrame(top_n_trending_hash_month(data_frame.hashtags ,-1))
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
        options=[{'label': i, 'value': i} for i in competitors ],
        value="KPMG",style={"width":"30vh" })],style={'display': 'flex','justify-content':'space-between','width':'46%','margin':"auto","padding":"30px"})

                             
    table1 = generate_table(tb)

    table2 = generate_table(lb)

    table= html.Div(id="table_area_compet",style = {'display': 'flex','justify-content':'space-between','width':'90%','margin':"auto"} )
    return html.Div([dashboard,alert , dropdown , table ])


def give_company_comparison_2(company = "KPMG"):
    with open('database/compet_database.json', 'r') as openfile: 
                data = json.load(openfile) 
    comp = pd.DataFrame(data['username'])
    competitors = comp.loc[comp.compet].screen_name.values
    self_account = comp.loc[~comp.compet].screen_name.values
    search_base = [{comp_:[comp_]} for comp_ in competitors]+[{"EY":list(self_account)}]

    ey = pd.DataFrame()
    for i in self_account:
        ey = pd.concat([ey,pd.read_csv('database/userdata/{}_user_profile.csv'.format(i))])
    
    
    data_frame = pd.read_csv('database/userdata/{}_user_profile.csv'.format(company))
    import ast 
    ey.hashtags = ey.hashtags.apply(ast.literal_eval)
    data_frame.hashtags = data_frame.hashtags.apply(ast.literal_eval)
    s= pd.DataFrame(top_n_trending_hash_month(data_frame.hashtags ,-1))
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
    


    table1 =html.Div([html.H2(" Leading Topics ",style={"font-size":"3rem","display":"flex","justify-content":"space-around","padding-bottom":"2pc"}) , 
                       generate_table(tb)],
                    style ={'width': '75vh','display': 'inline-block',"margin":"47px"} )

    table2 = html.Div([html.H2(" Lagging Topics ",style={"font-size":"3rem","display":"flex","justify-content":"space-around","padding-bottom":"2pc"}) , 
                       generate_table(lb)],
                    style ={'width': '75vh','display': 'inline-block',"margin":"47px"} )

    return [table1,table2]

