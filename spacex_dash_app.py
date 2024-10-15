# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
spacex_df['result']=spacex_df['class'].astype(str)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',options=[{'label':'All Sites','value':'ALL'},
                                                {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                                {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                                {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                                {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}],
                                                value='ALL',
                                                placeholder='place holder here',
                                                searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0:'0',500:'500',1000:'1000',1500:'1500',
                                                2000:'2000',2500:'2500',
                                                3000:'3000',3500:'3500',4000:'4000',4500:'4500',
                                                5000:'5000',5500:'5500',
                                                6000:'6000',6500:'6500',7000:'7000',7500:'7500',
                                                8000:'8000',8500:'8500',
                                                9000:'9000',9500:'9500',10000:'10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
                Input(component_id='site-dropdown',component_property='value'))
def get_pie_chart(value1):
    df = spacex_df
    if value1 == 'ALL':
        fig = px.pie(df,values='class',
        names='Launch Site',
        title='Total Success Lunch by Site')
        return fig
    else:
        fdf = df[df['Launch Site'] == value1]
        res=fdf['result'].value_counts()
        fig = px.pie(values=res,names=res.index,
        title=f'Launch Success Rate for {value1}')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])
def get_scatter_plot(value1,value2):
    df = spacex_df[(spacex_df['Payload Mass (kg)']>= value2[0])&(spacex_df['Payload Mass (kg)']<= value2[1])]
    if value1 == 'ALL':
        fig = px.strip(df, x='Payload Mass (kg)',y='class',color='Booster Version Category', 
        title='Correlation between Payload and Success for all Launch Sites')
        return fig
    else:
        df = spacex_df[(spacex_df['Payload Mass (kg)']>= value2[0])&(spacex_df['Payload Mass (kg)']<=value2[1])] 
        xdf=df[df['Launch Site']==value1]
        fig=px.strip(xdf,x='Payload Mass (kg)',y='class', 
        color='Booster Version Category',
        title=f'Correlation between Payload and Success for {value1}')
        return fig 

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
