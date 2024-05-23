import pandas as pd
from dash import dcc, html, Dash
import dash
# import plotly.express as px
# import plotly.graph_objects as go
import dash_auth

USER_PASS_MAPPING={
    "admin": "admin",
    "admin2": "password123"
}#Mongo pass: qsT3bfFDaS9zLjMv

#Initializing the App
app = Dash(__name__, pages_folder="pages", use_pages=True)

auth = dash_auth.BasicAuth(app, USER_PASS_MAPPING)
# App layout
app.layout = html.Div([    
    #Loop/and get all the page names
    html.Div(
        children=[
        dcc.Link(page['name'], href=page['relative_path'])\
        for page in dash.page_registry.values()], className= "navigation"
        ),
    html.H1('OLYMPIC BROADCAST DASHBOARD'),

    #Display the pages contents in the container
    dash.page_container
    
], className= "body")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
