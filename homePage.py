import dash_bootstrap_components as dbc
import dash_html_components as html
buzzing_img = "https://4.bp.blogspot.com/-dwlcXpHXzLM/T-poE-9fGNI/AAAAAAAACPc/7Z4w4rKLE4w/s400/trending+topics.png"
sentiment_url = "https://www.ntaskmanager.com/wp-content/uploads/2020/01/Sentiment-Analysis.png"
compet_url= "https://m.jagranjosh.com/imported/images/E/Articles/contestF.jpg"
hashtag_url ="https://cdn.telanganatoday.com/wp-content/uploads/2020/06/Hashtag.jpg"
map_url = "https://www.vuelio.com/uk/wp-content/uploads/2020/03/Influencer-Marketing-Smoking-Gun.jpg"
smart_recommender= "https://images.xenonstack.com/usecase/xenonstack-deep-learning-based-recommendation-system.png"
manage_sources = "https://miro.medium.com/max/8332/1*wK8k8Vo8_c6jdYIjUWL_Pw.png"
summary = "https://socialmediaweek.org/wp-content/blogs.dir/1/files/brand-blog-feature.jpg"
email_image="https://www.nicepng.com/png/detail/207-2075156_alert-icons-email-alert-icon-png.png"


sentiment_description = "Understand how users feel about this topic or your brand and compare it with how other big 4 companies are performing"

buzzing_description = "Track and analyze conversations around relevant topics gathered on the basis of the how frequent they are on Social Media "

compet_description = "Compare your performance on social to your competitors' to find new opportunities and see where are we leading or lagging."

campaign_description = "Report on the perception of a current or an upcoming campaign by tracking it's performance and relevant metrics"

influencer_description = "Identify top influencers, begin making contact and analyse how there tweets are performing on twitter"

recom_description=  "Suggest what are the key hashtags that should be used while making a post."

manage_sources_description = "Manage Sources is a brain / setting tool which stores user configuration and make changes in all other pages."

smart_link = "Blogs shared across the social media are ocean of information for any kind of analysis, So smart link summary extracts them all and show all the info on your fingertips"

email_description = "Want your Social Media report regularly on your Email ? Subscribe to the Newsletter in the section"

def make_card(img_url= sentiment_url, heading  = "Sentiment Analysis" , link ="sentiment",description=sentiment_description):
    card = dbc.Card(
        [
            dbc.CardImg(src=img_url, top=True),
            dbc.CardBody(
                [
                    html.H4(heading , className="card-title"),
                    html.P(
                        description,
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
    card_buzzword  = make_card(buzzing_img ,"Buzzing Topics" ,"/buzzing_topics" ,buzzing_description )
    card_compet = make_card(compet_url ,"Competitive Analysis" ,"/compet" , compet_description)
    card_hash = make_card(hashtag_url ,"Campaign Monitoring" ,"/hashtag" ,campaign_description)
    card_map = make_card(map_url ,"Influencer Monitoring" ,"/influencer" ,influencer_description)
    card_ai = make_card(smart_recommender ,"Smart Recommendation" ,"/recomend" ,recom_description)
    card_manage_sources = make_card(manage_sources ,"Manage Sources" ,"/managesources" ,manage_sources_description)
    card_summary = make_card(summary ,"Smart Link Summary" ,"/summary"  ,smart_link)
    card_email = make_card(email_image ,"Alerts" ,"/alert" ,email_description)
    
    cards_top = html.Div(className="cards",children=[card_manage_sources , card_hash , card_compet ],style={'display':"flex","justify-content":'space-between','margin':"30px",'padding':"10px"})
    
    cards_up = html.Div(className="cards",children=[ card  ,card_buzzword  , card_summary  ],style={'display':"flex","justify-content":'space-between','margin':"30px",'padding':"10px"})
    cards_down = html.Div(className="cards",children=[card_email , card_map  , card_ai ],style={'display':"flex","justify-content":'space-between','margin':"30px",'padding':"10px"})

    cards_deck = html.Div([cards_top , cards_up , cards_down],className="deck",style={'width':'90%','margin':'auto'})
    home_page_content= html.Div([dashboard  ,cards_deck])
    return home_page_content

