import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import json
import pandas as pd
import dash_bootstrap_components as dbc

def updateEmail(email,apps):
    '''
    Update the USER database displayed on the manage sources page
    '''
    if email:
        with open('database/email_database.json', 'r') as openfile: 
            data = json.load(openfile) 
        a=[]
        for em in data['email']:
            if em['email']!=email:
                a.append(em)
        a=a+[{'email':email,'apps':apps}]
        data['email']=a
        with open('database/email_database.json', 'w') as f:
            json.dump(data, f)
        return data
    else:
        with open('database/email_database.json', 'r') as openfile: 
            data = json.load(openfile) 
        return data
        



def generate_table_email(email,apps):
    data = updateEmail(email,apps)
    df=pd.DataFrame(data['email'])
    
    """
    Print generating new table
    """
    
#     with open('database/search_database.json', 'r') as openfile: 
#             search_database = json.load(openfile) 

#     tool_tip_data = [{'Tracking Entity':{'type': 'markdown','value':create_tabluated_data(ent['query'])}} for ent in search_database['search']]
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
    tooltip_data=[],tooltip_duration=None,
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



def email_page_content(dashboard):
    alert = dbc.Alert(
        [
            html.P("Alerts is like a weekly newsletter that gives the relevant details of any company you subscribed to. "),
            html.P("Just add your email id and list of companies for which you want the customized newsletter."),
        ]
    )
        
    with open('database/compet_database.json', 'r') as openfile: 
                    data = json.load(openfile) 
    comp = pd.DataFrame(data['username'])
    competitors = comp.loc[comp.compet].screen_name.values
    self_account = comp.loc[~comp.compet].screen_name.values
    search_base = [{comp_:[comp_]} for comp_ in competitors]+[{"EY":list(self_account)}]
    options = [list(i.keys())[0] for i in search_base]


    drop_down = html.Div([
        dcc.Dropdown(
            id='dropdown_track',
            options=[{'label': i, 'value': i} for i in options],
            value=options[0],
            multi=True
        ),
        html.Div(id='dd-output-container')
    ])

    hashtag_layout = html.Div(children = [html.H2("Add Email and tracking company",style={"background-color": "ghostwhite",
                                                    "padding": "16px",
                                                    "display": "flex",
                                                    'justify-content': "center",
                                                    "font-size": "27px",
                                                    "font-family": 'ui-serif'}),
                                      html.Div(id="track_search_",children = [dcc.Input(id="search_track",placeholder="type your email_id",style={'width':"41%"}),
                                      drop_down,
                                      html.Button("Submit", id='submit_track',n_clicks=0)],style={  "display": "flex",
                                                                                                        "justify-content": "center",
                                                                                                        "padding": "26px"}),
                                      html.Div(id='search_table_email')])


    return html.Div(children = [dashboard , alert , hashtag_layout])


