import pandas as pd
import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
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

text_input = html.Div(
    [dbc.Input(id="input_recom", placeholder="Type something...", type="text",style={'width':"70%",'padding-bottom':"20px"}),
    html.Br(),
    html.Div(id="table_recomm")])

dashboard = prepeare_Dashboard_content()
sentiment_content = prepeare_Sentiment_content(dashboard)
home_page_content= prepeare_HomePage_content(dashboard)
page_buzzwords_content = prepeare_Buzzword_content(dashboard)
page_compet_content = give_company_comparison(dashboard)
page_recommendation_content = [dashboard ,text_input]
page_hashtag_content = prepeare_Hashtag_content(dashboard)

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


leaderboard_content  = html.Div([dashboard  , get_leaderboard()])

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('table_area_compet', 'children'),
              [Input('xaxis-column_2', 'value')])
def change_comper(value):
    print(value)
    return give_company_comparison_2(value.lower())



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
        print("setniment page")
        return sentiment_content
    elif pathname == '/buzzing_topics':
        print("Buzzword page")
        return page_buzzwords_content
    elif pathname == '/hashtag':
        print("Buzzword page")
        return page_hashtag_content
    elif pathname == '/compet':
        print("Buzzword page")
        return page_compet_content
    elif pathname == '/recomend':
        print("Buzzword page")
        return page_recommendation_content
    
    elif pathname == '/influencer':
        print("Buzzword page")
        return leaderboard_content
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


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80)