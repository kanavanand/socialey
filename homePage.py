import dash_bootstrap_components as dbc
import dash_html_components as html
buzzing_img = "https://4.bp.blogspot.com/-dwlcXpHXzLM/T-poE-9fGNI/AAAAAAAACPc/7Z4w4rKLE4w/s400/trending+topics.png"
sentiment_url = "https://www.ntaskmanager.com/wp-content/uploads/2020/01/Sentiment-Analysis.png"
compet_url= "https://m.jagranjosh.com/imported/images/E/Articles/contestF.jpg"
hashtag_url ="https://cdn.telanganatoday.com/wp-content/uploads/2020/06/Hashtag.jpg"
map_url = "https://www.vuelio.com/uk/wp-content/uploads/2020/03/Influencer-Marketing-Smoking-Gun.jpg"
smart_recommender= "https://images.xenonstack.com/usecase/xenonstack-deep-learning-based-recommendation-system.png"

def make_card(img_url= sentiment_url, heading  = "Sentiment Analysis" , link ="/sentiment"):
    card = dbc.Card(
        [
            dbc.CardImg(src=img_url, top=True),
            dbc.CardBody(
                [
                    html.H4(heading , className="card-title"),
                    html.P(
                        "Some quick example text to build on the card title and "
                        "make up the bulk of the card's content.",
                        className="card-text"
                    ),
                    dbc.Button("Click for Analysis", color="primary",href=link),
                ]
            ),
        ],
        style={"width": "32rem",'padding':"10px","box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
      "transition": "0.3s"},
    )
    return card

    
def prepeare_HomePage_content(dashboard):
    card  = make_card()
    card_buzzword  = make_card(buzzing_img ,"Buzzing Topics" ,"/buzzing_topics" )
    card_compet = make_card(compet_url ,"Competitive Analysis" ,"/compet" )
    card_hash = make_card(hashtag_url ,"Campaign Monitoring" ,"/hashtag" )
    card_map = make_card(map_url ,"Influencer Monitoring" ,"/influencer" )
    card_ai = make_card(smart_recommender ,"Smart Recommendation" ,"/recomend" )
    
    
    
    
    cards_up = html.Div(className="cards",children=[card , card_buzzword  , card_compet ],style={'display':"flex","justify-content":'space-between','margin':"30px",'padding':"10px"})
    cards_down = html.Div(className="cards",children=[card_hash , card_map  , card_ai ],style={'display':"flex","justify-content":'space-between','margin':"30px",'padding':"10px"})

    cards_deck = html.Div([cards_up , cards_down],className="deck",style={'width':'90%','margin':'auto'})
    home_page_content= html.Div([dashboard  ,cards_deck])
    return home_page_content

