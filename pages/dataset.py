import pandas as pd
import dash
from dash import html, dash_table, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Page registration
dash.register_page(__name__, path='/dataset', name="DATASET")

#----------------------Dataset importation [start]----------------------------------------

data = 'Table2'  # data is the name of the sheet within pdData.xlsx

# read the excel file 
df = pd.read_excel('pdData.xlsx', sheet_name=data)

#Printing the df to inspect the dataframe
#print(df)  # You can uncomment to inspect in the terminal, [500 rows x 12 columns]

#----------------------Dataset importation [end]------------------------------------------

# Page layout (goes under the page container in the dash_app.py)
layout = html.Div(
    children=[
        html.H3("This is the dataset page"),
        "The dataset with sorting by duration is displayed here!",
        dcc.Dropdown(
            id='duration-sort', options=['Ascending', 'Descending'], value='Ascending'),
        dcc.Graph(id='table', figure={},style={
        'width': '100%',
        'height': '500px', 
        'margin-left':'-65px',
        'background-color':'Transparent'
        })
])

@callback(
    Output('table', 'figure'),
    [Input('duration-sort', 'value')]
)
def update_table(sort):
    if sort == 'Ascending':
        df_sorted = df.sort_values(by='duration')
    else:
        df_sorted = df.sort_values(by='duration', ascending=False)

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=list(df_sorted.columns),
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=[df_sorted[col] for col in df_sorted.columns],
                           fill_color='lavender',
                           align='left'))
        ],
        layout=go.Layout(width=1450,height=600))
    return fig