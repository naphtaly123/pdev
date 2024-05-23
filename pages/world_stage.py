import pandas as pd
import dash
from dash import html, dash_table, dcc, callback
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pymongo

# Page registration
dash.register_page(__name__, path='/world-stage', name="WORLD STAGE")

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

# Create world map
def create_world_map(data: pd.DataFrame) -> go.Figure:

    # Calculate the density of viewers for each country
    data['density'] = data['duration'] / data['duration'].max()

    world_map = px.choropleth(
        data,
        locations="country",
        locationmode="country names",
        color="density",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Plasma,
        range_color=(0, data['density'].max())
    )
    world_map.update_layout(
        legend=dict(y=1, x=0.78)
    )
    return world_map

# Page layout
def create_page_layout() -> html.Div:
    mongo_client = pymongo.MongoClient("mongodb+srv://naphtalynonofo:qsT3bfFDaS9zLjMv@cluster0.1vqtiu3.mongodb.net/")
    mongo_data = load_mongo_data(mongo_client, 'product_development', 'clients')
    
    # Create the filter for the broadcast column
    broadcast_options = [
        {'label': 'All', 'value': 'all'},
        {'label': 'Live', 'value': 'live'},
        {'label': 'Repeat', 'value': 'repeat'},
        {'label': 'Highlights', 'value': 'highlights'},
    ]

    broadcast_filter = dcc.RadioItems(
        id='broadcast-filter',
        options=broadcast_options,
        value='all',
        labelStyle={'display': 'inline-block'}
    )

    #Creating the world map
    world_map = create_world_map(mongo_data)

    # Update the world map based on the filter value

    @callback(
        Output('world-map', 'figure'),
        [Input('broadcast-filter', 'value')]
    )
    def update_world_map(filter_value):
        if filter_value == 'all':
            filtered_data = mongo_data
        else:
            filtered_data = mongo_data[mongo_data['broadcast'] == filter_value]
        return create_world_map(filtered_data)

    return html.Div(
        children=[
            html.Br(),
            html.H3("Density of view duration with all time max of "+ str(mongo_data['duration'].max()) + " Hours."),
            dcc.RadioItems(id='broadcast-filter', options=broadcast_options, value='all', labelStyle={'display': 'inline-block'}),
            dcc.Graph(id="world-map", figure=world_map, style={"height": "200%", "width": "100%"})
            
        ],
        className='body'
    )
    
#Defining the page layout.
layout = create_page_layout()