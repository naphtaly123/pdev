import pandas as pd
import dash
from dash import html, dash_table, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import plotly.subplots as sp

#Page regitration
dash.register_page(__name__, path='/', name="CONTENT PERFOMANCE")

#----------------------Dataset importation [start]----------------------------------------

data = 'Table2' #data is the name of the sheet within pdData.xlsx

#read the excel file 
df = pd.read_excel('pdData.xlsx', sheet_name='Table2')

#Printing the df to inspect the dataframe
#print(df) #You can uncomment to inspect in the terminal, [500 rows x 12 columns]


#----------------------Dataset importation [end]------------------------------------------

#Page layout(goes under the page container in the dash_app.py)
layout = html.Div([
    html.Br(),
    html.Div(
    children = [
    html.H3("This is the Control chart"),

    #Creating drop-down items for the SPC
    dcc.Dropdown(
        id='sport-dropdown',
        #For options: Get every unique value from the column sport
        options=[{'label': i, 'value': i} for i in df['sport'].unique()] + [{'label': 'All', 'value': 'All'}],
        value='All'
    ),

    # Graph component
    dcc.Graph(id='spc-chart', figure={})

    ], className='left_div'),

    html.Div(
    children = [
    html.H3("This is the Funnel"),

    #FOR OPTIONS: Get sports, from sport column
    dcc.Dropdown(
        id='sport2-dropdown',
        options=[{'label': i, 'value': i} for i in df['sport'].unique()],
        value='tennis'
    ),

    # Graph component
    dcc.Graph(id='funnel-chart', figure={})
    ], className='right_div')

])

# Define the callback
@callback(
    Output('spc-chart', 'figure'),
    [Input('sport-dropdown', 'value')]
)

def update_graph(selected_sport):
    if selected_sport == 'All':
        filtered_df = df.head(70)
    else:
        filtered_df = df[df['sport'] == selected_sport]
    mean_duration = filtered_df.groupby('start_time')['duration'].mean()
    # Calculate standard deviation for the entire dataset (not by group)
    std_duration = filtered_df['duration'].std()
    # Calculate control limits (assuming 3 standard deviations)
    control_limit1 = 0.1 * std_duration
    control_limit = 2.6 * std_duration

    upper_control_limit = mean_duration + control_limit1
    lower_control_limit = mean_duration - control_limit

    fig = sp.make_subplots(specs=[[{"type": "scatter"}]], shared_xaxes=True, vertical_spacing=0.01)

    # Add the mean duration line
    fig.add_trace(go.Scatter(x=mean_duration.index, y=mean_duration.values, name='Mean Duration', mode='lines'), row=1, col=1)

    # Add the control limits (horizontal lines)
    fig.add_trace(go.Scatter(x=[min(filtered_df['start_time']), max(filtered_df['start_time'])], y=[upper_control_limit.values[0], upper_control_limit.values[0]], line_width=2, line_color='red', name='UCL'))
    fig.add_trace(go.Scatter(x=[min(filtered_df['start_time']), max(filtered_df['start_time'])], y=[lower_control_limit.values[0], lower_control_limit.values[0]], line_width=2, line_color='red', name='LCL'))

    # Add the data points (scatter plot)
    fig.add_trace(go.Scatter(x=filtered_df['start_time'], y=filtered_df['duration'], mode='markers', name='Individual Durations'), row=1, col=1)

    fig.update_layout(
        title='View duration by start time',
        xaxis=dict(title='Start Time'),
        yaxis=dict(title='Duration'),
        yaxis2=dict(overlaying='y', side='right'),
        height=400,
        width=700,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True
        )

    return fig

@callback(
    Output('funnel-chart','figure'),
    [Input('sport2-dropdown','value')]
)
def update_funnel_chart(selected_sport):
    filtered_df = df[df['sport'] == selected_sport]
    fig = px.funnel(
        filtered_df,
        x='broadcast',
        y='duration',
        color='broadcast'
    )
    return fig