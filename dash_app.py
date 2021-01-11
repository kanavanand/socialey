import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pandas as pd
import json
import dash_table
img_url = "https://www.ntaskmanager.com/wp-content/uploads/2020/01/Sentiment-Analysis.png"
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from sentiment import prepeare_Sentiment_content , update_sentiment_trend
from commonDashboard import prepeare_Dashboard_content
from homePage import prepeare_HomePage_content
from hashtag import prepeare_Hashtag_content,hashtag_graphs
from competitive import give_company_comparison, give_company_comparison_2
from buzzwords import prepeare_Buzzword_content,sentiment_distribution_word,wordcloud_bigram
from manageSources import (prepeare_ManageSources_content,updateSearchDataBase , searchbaseTable ,updateCompetDataBase,
                             searchUserKeyword ,makeCard ,PreventUpdate )

from summary import (prepeare_SummaryPage_content , summarize_article , generate_tableURL)
from email_tracker import email_page_content , generate_table_email
import ast 
import numpy as np


alert_recom = dbc.Alert(
        [
            html.H4("Well done!", className="alert-heading"),
            html.P(
                "This is a success alert with loads of extra text in it. So much "
                "that you can see how spacing within an alert works with this "
                "kind of content."
            ),
            html.Hr(),
            html.P(
                "Let's put some more text down here, but remove the bottom margin",
                className="mb-0",
            ),
        ]
    )
alert_influencer =dbc.Alert(
        [
            html.H4("Well done!", className="alert-heading"),
            html.P(
                "This is a success alert with loads of extra text in it. So much "
                "that you can see how spacing within an alert works with this "
                "kind of content."
            ),
            html.Hr(),
            html.P(
                "Let's put some more text down here, but remove the bottom margin",
                className="mb-0",
            ),
        ])



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



text_input = html.Div(
    [dbc.Input(id="input_recom", placeholder="Type something...", type="text",style={'width':"70%",'padding-bottom':"20px"}),
    html.Br(),
    html.Div(id="table_recomm")])


dashboard = prepeare_Dashboard_content()
manage_sources = prepeare_ManageSources_content(dashboard)
home_page_content= prepeare_HomePage_content(dashboard)
page_recommendation_content = [dashboard,alert_recom ,text_input]





def update_recent_tweets():
    df = data[['date','tweet','sentiment']]
    table= generate_table(df, max_rows=10)

standard_Style = {'width': '75vh', 'height': '45vh','display': 'inline-block',
                                                             "box-shadow":"0 8px 16px 0 rgba(0,0,0,0.2)"}

chain_list_df = pd.read_pickle('supply_chain_4.pkl') 

def chain_splitting(x):
    try:
        tags = x.split(',')
        print("these are tags",tags)
        data_ = chain_list_df[chain_list_df.arranged.apply(lambda x: False==any([i for i in tags if i not in x.split('|')]))]

        table1 = html.Div([html.H2(" Leading Topics ",style={"font-size":"3rem","display":"flex","justify-content":"space-around","padding-bottom":"2pc"}) , 
                       dbc.Table.from_dataframe(data_.head(30), striped=True, bordered=True, hover=True)],
                    style ={'width': '100vh','display': 'inline-block',"margin":"70px"} )


        return table1
    except:
        data_ = chain_list_df
        table1 = html.Div([html.H2(" Leading Topics ",style={"font-size":"3rem","display":"flex","justify-content":"space-around","padding-bottom":"2pc"}) , 
                       dbc.Table.from_dataframe(data_.head(30), striped=True, bordered=True, hover=True)],
                    style ={'width': '100vh','display': 'inline-block',"margin":"70px"}  )


        return table1

        


import itertools
from hackpion.EyMiner import getUserNameData
users =['Mark_Weinberger', 'Carmine_DiSibio', 
       'MilkenInstitute', 'Julie_Teigland', 'AndyBaldwin_', 'AlisonKayEY',
       'EY_Africa', 'EY_US', 'Jeff__Wong',
       'BethBrooke_EY',  'EY_India', 'KellyGrierEY', 'ShaunCrawfordEY',
       'KristinaRRogers', 'SteveKrouskos']



def get_leaderboard():
    userData = pd.DataFrame()
    for user in users:
        filePath = "userdata/{}_user_profile.csv".format(user)
        userData = pd.concat([userData, pd.read_csv(filePath)])

    dataframe = pd.DataFrame(userData.groupby(by='username').id.count())
    dataframe['Total Likes'] = userData.groupby(by='username').likes_count.sum()
    dataframe['Retweets Likes'] = userData.groupby(by='username').retweets_count.sum()
    leaderboard = dataframe.reset_index()
    leaderboard.columns =['Username', 'Total Tweets', 'Total Likes', 'Total Retweets']
    table1 = html.Div([html.H2(" Top Influencers ",style={"font-size":"3rem","display":"flex","justify-content":"space-around","padding-bottom":"2pc"}) , 
               dbc.Table.from_dataframe(leaderboard, striped=True, bordered=True, hover=True)],
            style ={'width': '55vh','display': 'inline-block',"margin":"70px"} )
    return table1


leaderboard_content  = html.Div([dashboard ,alert_influencer , get_leaderboard()])    


import itertools
from hackpion.EyMiner import getUserNameData
users =['Mark_Weinberger', 'Carmine_DiSibio', 
       'MilkenInstitute', 'Julie_Teigland', 'AndyBaldwin_', 'AlisonKayEY',
       'EY_Africa', 'EY_US', 'Jeff__Wong',
       'BethBrooke_EY',  'EY_India', 'KellyGrierEY', 'ShaunCrawfordEY',
       'KristinaRRogers', 'SteveKrouskos']


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
###################################### MANAGE SOURCES START ######################################

########################## Scrape Search Tweets and update in table##########################
@app.callback(
     dash.dependencies.Output('search_table_2', 'children'),
    [dash.dependencies.Input('submit_hashtag', 'n_clicks')],
    [dash.dependencies.State('search_hashtag', 'value')])
def update_search_content(n_clicks,value):
    updateSearchDataBase(value)
    print("Hashtag Search for :",value)
    return searchbaseTable()   


########################## Scrape ey username and update cards ##########################
@app.callback(
    dash.dependencies.Output('ey_cards', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('my-dynamic-dropdown', 'value'),dash.dependencies.State('my-dynamic-dropdown', 'data')])
def update_EY_output(n_clicks, value,data):
    updateCompetDataBase(value)
    print("Updating cards for EY and adding",value)
    cards=[]
    with open('database/compet_database.json', 'r') as openfile: 
        data = json.load(openfile) 
    for user in data['username']:
        if user['compet']==False:
            cards.append(makeCard(user))
    return cards  

    

########################## Scrape COMP username and update cards ##########################
@app.callback(
    dash.dependencies.Output('comp_cards', 'children'),
    [dash.dependencies.Input('submit-val-comp', 'n_clicks')],
    [dash.dependencies.State('comp-dynamic-dropdown', 'value'),dash.dependencies.State('my-dynamic-dropdown', 'data')])
def update_output_comp(n_clicks, value,data):
    updateCompetDataBase(value,True)
    print("Updating cards for compet")
    cards=[]
    with open('database/compet_database.json', 'r') as openfile: 
        data = json.load(openfile) 
    for user in data['username']:
        if user['compet']==True:
            cards.append(makeCard(user))
    return cards        




########################## Update dropdown on EY user search ##########################
@app.callback(
    dash.dependencies.Output("my-dynamic-dropdown", "options"),
    [dash.dependencies.Input("my-dynamic-dropdown", "search_value")])
def update_options(search_value):
    if not search_value:
        raise PreventUpdate
    return searchUserKeyword(search_value)


########################## Update dropdown on COMP user search ##########################
@app.callback(
    dash.dependencies.Output("comp-dynamic-dropdown", "options"),
    [dash.dependencies.Input("comp-dynamic-dropdown", "search_value")],
)
def update_options_comp(search_value):
    if not search_value:
        raise PreventUpdate
    return searchUserKeyword(search_value,True)
###################################### MANAGE SOURCES END ######################################




@app.callback(Output('table_area_compet', 'children'),
              [Input('xaxis-column_2', 'value')])
def change_comper(value):
    print(value)
    return give_company_comparison_2(value)





@app.callback(Output('table_recomm', 'children'),
              [Input('input_recom', 'value')])
def hashrecommendation(value):
    print(value)
    return chain_splitting(value)



    

@app.callback(Output("hashtag_full", "children"),
              Input('submit-button-state', 'n_clicks'),
              State("switches-input", "value"),
              State('input-1-state', 'value'))
def hashtag_value_taker(n_clicks,pain_point, value):
    print(value,pain_point)
    fig_1 , fig_2 ,cards ,table= hashtag_graphs(value,pain_point)
    up_row = html.Div([cards , html.Div(table,style={'width': '75vh', 'height': '32vh','display': 'inline-block',
                                                             "box-shadow":"0 8px 16px 0 rgba(0,0,0,0.2)"})],style={'display': 'flex','justify-content':'space-between','width':'90%','margin':"auto","padding-bottom":"50px"})
    down_row = html.Div(children=[
            dcc.Graph(id='user_name_hashtag',figure=fig_1,style=standard_Style),
            dcc.Graph(id='trend_hashtag',figure=fig_2,style=standard_Style)],
            style={'display': 'flex','justify-content':'space-between','width':'90%','margin':"auto"})
    
    hashtag_an = html.Div([up_row,down_row])
    return hashtag_an



@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/sentiment':
        sentiment_content = prepeare_Sentiment_content(dashboard)
        print("setniment page")
        return sentiment_content
    elif pathname == '/buzzing_topics':
        page_buzzwords_content = prepeare_Buzzword_content(dashboard)
        print("Buzzword page")
        return page_buzzwords_content
    elif pathname == '/hashtag':
        page_hashtag_content = prepeare_Hashtag_content(dashboard)
        print("Buzzword page")
        return page_hashtag_content

    elif pathname == '/compet':
        page_compet_content = give_company_comparison(dashboard)
        print("Buzzword page")
        return page_compet_content

    elif pathname == '/recomend':
        print("Buzzword page")
        return page_recommendation_content
    
    elif pathname == '/influencer':
        print("Buzzword page")
        return leaderboard_content
    
    elif pathname == '/managesources':
        print("Manage Sources page")
        return manage_sources
    elif pathname == '/summary':
        summary_page_content=prepeare_SummaryPage_content(dashboard)
        return summary_page_content
    elif pathname == '/alert':
        email_page = email_page_content(dashboard)
        return email_page
    
    else:
        return home_page_content
    
    



    
@app.callback(
    Output('words_overall_ey_graph', 'figure'),
    [Input('pie', 'clickData')])

def display_click_data(clickData):
    try:
        print("Processing click data.",clickData)
        topic_selected = clickData['points'][0]['label']
        return wordcloud_bigram(topic_selected)
    except:
        return wordcloud_bigram("covid")


@app.callback(
    Output('pie_sentiment', 'figure'),
    [Input('pie', 'clickData')])

def display_click_data_2(clickData):
    try:
        print("Processing click data.",clickData)
        topic_selected = clickData['points'][0]['label']
        return sentiment_distribution_word(topic_selected)
    except:
        return sentiment_distribution_word("covid")

@app.callback(
    Output('example-graph_2', 'figure'),
    [Input('multi_select_option', 'value') ,Input('timeframe_selection', 'value') ])
def update_sentiment_trend_(selected_options , timeframe):
    return update_sentiment_trend(selected_options , timeframe)
################################# summary _content ############################################

@app.callback(
    dash.dependencies.Output('container_LinkTable', 'children'),
    [dash.dependencies.Input('dropdown_summary', 'value')])
def update_output_summary(value):
    return generate_tableURL(value)

@app.callback(
     dash.dependencies.Output('container_summary', 'children'),
    [dash.dependencies.Input('submit_URL', 'n_clicks')],
    [dash.dependencies.State('url_search_input', 'value')])
def update_search_content_summary(n_clicks,value):

    return summarize_article(value)  


@app.callback(
     dash.dependencies.Output('container_blog', 'children'),
    [dash.dependencies.Input('submit_URL_bog', 'n_clicks')],
    [dash.dependencies.State('url_search_input', 'value')])

def update_search_content1_summary(n_clicks,value):
    return summarize_article(value,blog=True)  

##################################################################################################################
@app.callback(
    dash.dependencies.Output('search_table_email', 'children'),
    [dash.dependencies.Input('submit_track', 'n_clicks')],
dash.dependencies.State('search_track','value'),dash.dependencies.State('dropdown_track','value'))
def update_email(clic,value1,value2):
    print(clic,value1,value2)
    return generate_table_email(value1,value2)


##################################################################################################################



if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80)