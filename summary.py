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
import itertools
import ast
import json
import pandas as pd
import nltk
nltk.download('punkt')

def getURLpopulIndex(competitors):
    return df

def  tabulatedToolData(dataCombined , hashtag_):
    data_combined = dataCombined.loc[dataCombined.hashtags.apply(lambda x: any([i for i in x if hashtag_ == i.lower()]))]
    leaderBoard= data_combined.groupby(by='Company').hashtags.count().sort_values(ascending=False).reset_index()
    leaderBoard['Rank']= np.arange(1,leaderBoard.shape[0]+1)
    leaderBoard.columns = ['Company', 'Count','Rank' ]
    leaderBoard = leaderBoard[['Rank' , 'Company', 'Count']]
    return leaderBoard.set_index('Rank').to_markdown()

def generate_tableURL(competitors,drp=False):
    with open('database/compet_database.json', 'r') as openfile: 
        data = json.load(openfile) 
    comp = pd.DataFrame(data['username'])
#     competitors = comp.loc[comp.compet].screen_name.values
    self_account = comp.loc[~comp.compet].screen_name.values


    print(competitors)
    if "EY" in competitors:
        competitors.remove('EY')
        competitors=competitors+list(self_account)
    print(competitors)
    compet = pd.DataFrame()
    for i in competitors:
        tmp=pd.read_csv('database/userdata/{}_user_profile.csv'.format(i))
        tmp['Company']=i
        compet = pd.concat([compet,tmp])
    compet.urls = compet.urls.apply(ast.literal_eval)
    compet.hashtags = compet.hashtags.apply(ast.literal_eval)
    s= pd.Series(itertools.chain.from_iterable(compet.urls)).value_counts()
    if drp:
        return s.head(15).index
    like_=[]
    tweet_=[]
    hashtags_=[]
    
    for i in s.head(15).index:
        tmp = compet.loc[compet.urls.apply(lambda x: i in x)][['tweet','likes_count','hashtags']]
        like_.append(sum(tmp.likes_count.values))
        
        tweet_.append(tmp.tweet.values[0])
        hashtags_.append("#"+ " #".join(pd.Series(itertools.chain.from_iterable(tmp.hashtags)).value_counts().index[:5]))
    

    df = s.head(15).reset_index()
    df['Popullarity Index'] =like_
    df.columns = ["URL","Count Posted", "Popullarity Index"]


#     """
#     Print generating new table
#     """
    
    tool_tip_data = [{'URL':{'type': 'markdown','value':i}} for i in hashtags_]
    print(tool_tip_data)
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



import re
import nltk

def summarize_article(url,blog=False):
    if url:
        article_text = give_content_URL(url)

        if len(article_text)>100:
            if blog:
                return article_text
            article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
            article_text = re.sub(r'\s+', ' ', article_text)
            formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
            formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
            sentence_list = nltk.sent_tokenize(article_text)
            stopwords = nltk.corpus.stopwords.words('english')

            word_frequencies = {}
            for word in nltk.word_tokenize(formatted_article_text):
                if word not in stopwords:
                    if word not in word_frequencies.keys():
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1
            maximum_frequncy = max(word_frequencies.values())

            for word in word_frequencies.keys():
                word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

            sentence_scores = {}
            for sent in sentence_list:
                for word in nltk.word_tokenize(sent.lower()):
                    if word in word_frequencies.keys():
                        if len(sent.split(' ')) < 30:
                            if sent not in sentence_scores.keys():
                                sentence_scores[sent] = word_frequencies[word]
                            else:
                                sentence_scores[sent] += word_frequencies[word]
            import heapq
            summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)

            summary = '\n'.join(summary_sentences)
            return summary
        else:
            return "None"
    else:
        return "None"

import requests
from bs4 import BeautifulSoup

def give_content_URL(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    text=''
    for i in soup.find_all('p'):
        text= text + i.text.strip()
    return text

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]



import dash
import dash_html_components as html
import dash_core_components as dcc

def prepeare_SummaryPage_content(dashboard):
    alert = dbc.Alert(
        [
            html.P("Smart Link Summary helps fetch all the recent top blogs  for companies you feed in search bar and apply a specialized summarizer to get a ready summary out of the blog"),
            html.P("Hover over the link to get the idea of content inside that blog by seeing hashtags used in tweet."),
            html.P("For input links of posts, use Ctrl+C and Ctrl+V. from the links beside, Get a summary or full blog, as per your choice")

        ]
    )
    with open('database/compet_database.json', 'r') as openfile: 
        data = json.load(openfile) 
    comp = pd.DataFrame(data['username'])
    competitors = comp.loc[comp.compet].screen_name.values
    self_account = comp.loc[~comp.compet].screen_name.values
    search_base = [{comp_:[comp_]} for comp_ in competitors]+[{"EY":list(self_account)}]

    summary_content = html.Div([
        html.H2("Top Links with Real Time Summarizer"),
        html.Div(children = [dcc.Dropdown(
            id='dropdown_summary',
            options=[{'label': list(i.keys())[0], 'value': list(i.keys())[0]} for i in search_base],
            value=list(search_base[0].keys()),
                multi=True,style={'width':'50%'}

        ),html.H4("Copy Paste link from Table in search Feild ")],style={'display':"flex",'justify-content': 'space-between','width': '81%'}),
        html.Div(children = [
        html.Div(id='container_LinkTable', style={'width':"67%"}),
        html.Div(id="url_search",children = [
                                             dcc.Input(id="url_search_input",placeholder="Input hashtag you want to track",style={'width':"41%"}),
                                             html.Button("Summary", id='submit_URL',n_clicks=0),
                                             html.Button("Full Blog", id='submit_URL_bog',n_clicks=0),
                                             html.H4("Summary of Blog"),
                                             html.Div(id='container_summary'),
                                             html.H4("Complete Blog "),
                                             html.Div(id='container_blog')],
                 style={'width':"45%"}
            )
                            ],style={'display': 'flex','justify-content': 'space-between','width': '90%','padding':'10px'})

    ])
    return html.Div(children= [dashboard,alert , summary_content])

