from sklearn.feature_extraction.text import*
import nltk
nltk.download('stopwords')

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
import json

from nltk.corpus import stopwords
import operator
allStopwords = set(stopwords.words('english'))
import numpy as np
from sentiment import preprocessData
# ey = preprocessData(pd.read_csv('../data/ey_news.csv'))
with open('database/compet_database.json', 'r') as openfile: 
            data = json.load(openfile) 
comp = pd.DataFrame(data['username'])
competitors = comp.loc[comp.compet].screen_name.values
self_account = comp.loc[~comp.compet].screen_name.values
search_base = [{comp_:[comp_]} for comp_ in competitors]+[{"EY":list(self_account)}]
    
ey = pd.DataFrame()
for i in self_account:
    ey = pd.concat([ey,pd.read_csv('database/userdata/{}_user_profile.csv'.format(i))])

import ast 
ey.hashtags = ey.hashtags.apply(ast.literal_eval)
ey.mentions = ey.mentions.apply(ast.literal_eval)



def give_buzzing_word( data , TOPIC ):
        all_sentences = data.loc[data.hashtags.apply(lambda x: TOPIC in [i.lower() for i in x])].cleaned_review.unique()
        st = " ".join(all_sentences)
        cvector = CountVectorizer(min_df = 0.0,  ngram_range=(2,2),stop_words=list(allStopwords),max_features=100)
        vec = cvector.fit_transform([st])
        dic = dict(zip(cvector.get_feature_names(),list(np.squeeze(np.array(vec.todense())))))
        refined=[]
        WORDLIMIT = 50
        for i in dic.keys():
            if len(set(i.split(" ")))>1:
                continue
            else:
                refined.append(i)
        for i in refined:
            del(dic[i]) 
        freq_dic =pd.DataFrame(sorted(dic.items(),key=operator.itemgetter(1),reverse=True),columns=['words','freq'])
        freq_dic['set_n'] = freq_dic.words.apply(lambda x: set(x.split(" "))).astype(str)
        new_freq = pd.DataFrame(freq_dic.groupby(by='set_n').words.apply(lambda x: x.values[0]))
        new_freq['frequency'] = pd.DataFrame(freq_dic.groupby(by='set_n').freq.sum())
        df=new_freq.reset_index(drop=True).sort_values(by='frequency',ascending=False)
        tf=TfidfVectorizer()
        df['tf_score'] =np.squeeze(np.array(tf.fit_transform(df.words.values).todense())).sum(axis=1)
        from sklearn.preprocessing import MinMaxScaler
        mm=MinMaxScaler()
        arr=mm.fit_transform(df[['frequency','tf_score']])
        df['final_score']  = arr[:,0]*0.15+arr[:,1]*0.85
        df.sort_values(by='final_score',ascending=False,inplace=True)
        df = df.head(WORDLIMIT)
        df = df.astype(str)
        return df.head(20)
    
import itertools
def company_buzzword():
    all_tags = list(itertools.chain.from_iterable(ey.hashtags.values))

    all_tags_lower = [i.lower() for i in all_tags if i.lower() not in ["rt" , "coronavirus","covid"]]

    MainTopic = pd.DataFrame(pd.Series(all_tags_lower).value_counts()).reset_index().head(10)
    MainTopic.columns =['Hot Topics' , 'frequency']
    MainTopic['Hot Topics'] = MainTopic['Hot Topics']
    fig = px.bar(MainTopic, x="frequency", y="Hot Topics", title='Buzzing Topics from Social Media',
                 orientation='h')
    fig.update_layout(
   
    
    plot_bgcolor='white'
)

    
    return fig



import plotly.graph_objects as go

def sentiment_distribution_word(hashtag):
    data = ey.loc[ey.hashtags.apply(lambda x: str(hashtag) in [i.lower() for i in x])]
    print(data.shape)
    colors = [ 'lightgreen', 'mediumturquoise', 'darkorange' ]

    fig = go.Figure(data=[go.Pie(labels=data.sentiment.value_counts().index,
                                 values=data.sentiment.value_counts().values,hole=0.4 ,title="Sentiment")])
    
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    return fig



def wordcloud_bigram(word="#covid19"):
    try:
        BuzzingWordsInTopic =  give_buzzing_word(ey,word).head(12)
        fig = px.treemap(BuzzingWordsInTopic, path=['words'], values='frequency',title='Trending Keywords')
        return fig
    except:
        word="#covid19"
        BuzzingWordsInTopic =  give_buzzing_word(ey,word).head(12)
        fig = px.treemap(BuzzingWordsInTopic, path=['words'], values='frequency',title='Trending Keywords')
        return fig
    



    
def prepeare_Buzzword_content(dashboard):
    alert = dbc.Alert(
    [
        html.P("List of findings of hot topics along with their frequency"),
        html.P("Clicking on any particular hashtag from the bars in the 1st  chart results in a display of buzzwords around that hashtag in the 2nd chart. "),
        html.P("Donut chart to represent sentiments for a particular hashtag from 1st chart.")
    ]
    )

    buzzwords = html.Div(children=[
            dcc.Graph(id='pie',figure=company_buzzword(),style={'width': '75vh', 'height': '55vh','display': 'inline-block',
                                                             "box-shadow":"0 8px 16px 0 rgba(0,0,0,0.2)"}),

            dcc.Graph(id='words_overall_ey_graph',style={'width': '75vh', 'height': '55vh','display': 'inline-block',
                                                             "box-shadow":"0 8px 16px 0 rgba(0,0,0,0.2)"})
        ],style={'display': 'flex','justify-content':'space-between','width':'90%','margin':"auto"})


    buzzwords_down = html.Div(children=[
            dcc.Graph(id='pie_sentiment',style={'width': '75vh', 'height': '55vh','display': 'inline-block','padding-top':'100px',
                                                             "box-shadow":"8px 8px 16px 0 rgba(0,0,0,0.2)"})

    #         dcc.Graph(id='words_overall_ey_graph',style={'width': '80vh', 'height': '60vh','display': 'inline-block',
    #                                                          "box-shadow":"0 8px 16px 0 rgba(0,0,0,0.2)"})
        ],style={'display': 'flex','justify-content':'space-between','width':'90%','margin':"auto"})



    page_buzzwords_content = html.Div([dashboard ,alert , html.Div([buzzwords , buzzwords_down],style={'padding':"30px"}) ])
    return page_buzzwords_content
