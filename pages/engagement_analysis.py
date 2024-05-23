import dash
from dash import html, dash_table, dcc, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import numpy as np
import pymongo

# Page registration
dash.register_page(__name__, path='/engagement-analysis', name="ENGAGEMENT")

# # ----------------------Dataset importation [start]----------------------------------------

# data = 'Table2'  # data is the name of the sheet within pdData.xlsx

# # read the excel file 
# data = pd.read_excel('pdData.xlsx', sheet_name=data)

# # Printing the df to inspect the dataframe
# # print(df)  # You can uncomment to inspect in the terminal, [500 rows x 12 columns]

# # ----------------------Dataset importation [end]------------------------------------------

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

def create_bar_chart(data: pd.DataFrame) -> html.Div:
    bar_chart = html.Div(
        children=[
        dcc.Dropdown(
                id='sport-filter',
                options=[{'label': i, 'value': i} for i in data['broadcast'].unique()],
                value='All',
                style={'width': '50%', 'margin-left': '10px','margin-top': '1px'}
            ),
        dcc.Graph(id='bar-chart',style={'width': '50%', 'margin': '0 auto','float':'left'})
        ]
    )

    @callback(
        Output('bar-chart', 'figure'),
        [[Input('sport-filter', 'value')]]
    )
    def update_bar_chart(data: pd.DataFrame) -> html.Div:
        data = 'Table2'  # data is the name of the sheet within pdData.xlsx
        # read the excel file 
        data = pd.read_excel('pdData.xlsx', sheet_name=data)
        fig = go.Figure(
            data=[
                go.Bar(x=data['country'], y=data.groupby('country')['duration'].sum(), name=sport) for sport in data['sport'].unique()
            ],
            layout=go.Layout(
                title='View duration by country',
                barmode='stack',
                xaxis=dict(title='Country'),
                yaxis=dict(title='Duration')
            )
        )
        return fig
    return bar_chart

def create_scatter_plot(data: pd.DataFrame) -> html.Div:
    scatter_plot = html.Div(
        children=[
            dcc.Dropdown(
                id='sport-filter',
                options=[{'label': i, 'value': i} for i in data['sport'].unique()],
                value='All',
                style={'width': '50%', 'margin': '0 auto','float':'right','margin-top': '-20px'}
            ),
            dcc.Graph(id='scatter-plot',style={'width': '50%', 'margin': '0 auto','float':'right'})
        ]
    )

    @callback(
        Output('scatter-plot', 'figure'),
        [Input('sport-filter', 'value')]
    )
    def update_scatter_plot(sport):
        data = 'Table2'  # data is the name of the sheet within pdData.xlsx
        # read the excel file 
        data = pd.read_excel('pdData.xlsx', sheet_name=data)
        if sport == 'All':
            data = data[['duration']]
            x = np.arange(len(data))
            x_labels = [f'User {i+1}' for i in range(len(data))]
        else:
            data = data[data['sport'] == sport][['duration']]
            x = np.arange(len(data))
            x_labels = [f'User {i+1}' for i in range(len(data))]

        fig = go.Figure(
            data=[go.Scatter(x=x, y=data['duration'].values, mode='markers')],
            layout=go.Layout(
                title='View duration by no of views',
                xaxis=dict(
                    title='User',
                    tickvals=np.arange(0, len(x), 100),
                    ticktext=x_labels[::100]
                ),
                yaxis=dict(title='Duration')
            )
        )
        return fig
    return scatter_plot

def create_page_layout():
    mongo_client = pymongo.MongoClient("mongodb+srv://naphtalynonofo:qsT3bfFDaS9zLjMv@cluster0.1vqtiu3.mongodb.net/")
    mongo_data = load_mongo_data(mongo_client, 'product_development', 'clients')

    return html.Div(
        children=[
        create_bar_chart(mongo_data),
        create_scatter_plot(mongo_data)
        ])
 
layout = create_page_layout()