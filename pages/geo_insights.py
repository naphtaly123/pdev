import pandas as pd
import dash
from dash import html, dash_table, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pymongo

#Page regitration
dash.register_page(__name__, path='/geo-insights', name="GEO-INSIGHTS")


#----------------------Dataset importation [start]----------------------------------------

data = 'Table2' #data is the name of the sheet within pdData.xlsx

#read the excel file 
df = pd.read_excel('pdData.xlsx', sheet_name=data)

#Printing the df to inspect the dataframe
#print(df) #You can uncomment to inspect in the terminal, [500 rows x 12 columns]

#----------------------Dataset importation [end]------------------------------------------


# Load data from MongoDB
def load_mongo_data(client: pymongo.MongoClient, db_name: str, collection_name: str) -> pd.DataFrame:
    try:
        db = client[db_name]
        collection = db[collection_name]
        data = list(collection.find())
        return pd.DataFrame(data)
    except pymongo.errors.PyMongoError as e:
        print(f"Error: {e}")
        return pd.DataFrame()

# Create card visuals
def create_card_visuals(data: pd.DataFrame) -> html.Div:
    views = html.Div(
        children=[
            html.H6('Total Views:', style={'color': '#000000'}),
            html.H3(data.shape[0], style={'color': '#000000'})
        ],
        style={'width': '25%', 'display': 'inline-block'}
    )
    mean = html.Div(
        children=[
            html.H6('Mean Duration:', style={'color': '#000000'}),
            html.H3(data['duration'].mean(), style={'color': '#000000'})
        ],
        style={'width': '25%', 'display': 'inline-block'}
    )
    high = html.Div(
        children=[
            html.H6('Max Duration:', style={'color': '#000000'}),
            html.H3(data['duration'].max(), style={'color': '#000000'})
        ],
        style={'width': '25%', 'display': 'inline-block'}
    )

    low = html.Div(
        children=[
            html.H6('Min Duration:', style={'color': '#000000'}),
            html.H3(data['duration'].min(), style={'color': '#000000'})
        ],
        style={'width': '25%', 'display': 'inline-block'}
    )

    return html.Div(
        children=[views, mean, high, low],
        style={'display': 'flex', 'justify-content': 'space-around','background-color':'grey'}
    )

def create_bar_chart(data: pd.DataFrame) -> html.Div:
    bar_chart = html.Div(
        children=[
            dcc.Dropdown(
                id='continent-filter',
                options=[{'label': i, 'value': i} for i in data['continent'].unique()],
                value='All',
                style={'width': '50%', 'margin': '0 auto'}
            ),
            dcc.Graph(id='bar-chart1', figure={})
        ]
    )

    @callback(
        Output('bar-chart1', 'figure'),
        [Input('continent-filter', 'value')]
    )
    def update_bar_chart(continent):
        if continent == 'All':
            data = df[['country', 'duration']]
        else:
            data = df[df['continent'] == continent][['country', 'duration']]

        fig = go.Figure(
            data=[go.Bar(x=data['country'], y=data['duration'])],
            layout=go.Layout(
                title='Duration of View Time by Country',
                xaxis=dict(title='Country'),
                yaxis=dict(title='Duration')
            )
        )

        return fig

    return bar_chart


# Page layout
def create_page_layout() -> html.Div:
    mongo_client = pymongo.MongoClient("mongodb+srv://naphtalynonofo:qsT3bfFDaS9zLjMv@cluster0.1vqtiu3.mongodb.net/")
    mongo_data = load_mongo_data(mongo_client, 'product_development', 'clients')
    card_visuals = create_card_visuals(mongo_data)
    bar_chart = create_bar_chart(mongo_data)
    return html.Div(
        children=[
            html.Br(),
            html.H3("General GEO-INSIGHTS"),
            card_visuals,
            bar_chart
        ],
        className='body'
    )
    
#Defining the page layout.
layout = create_page_layout()
