# Import required libraries
from tkinter import Y
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
from pathlib import Path


# Read the spacex data into pandas dataframe
file = Path("C:\HomeCloud\Learning Dropbox\IBM\Data Science\Applied Data Science Capstone\Week 3\spacex_launch_dash.csv")

spacex_df = pd.read_csv(file,header=0)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
print(max_payload)
print(min_payload)

fig_pie = px.pie(spacex_df, title='XXX', names="Launch Site")
fig_scatter = px.scatter(spacex_df, title="Scatter", x="Payload Mass (kg)", y="class")


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div(
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                ],
                                value="ALL",
                                placeholder="Select Site",
                                searchable=True
                                )),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                html.Div(dcc.Graph(id='success-pie-chart',figure= fig_pie)),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id='payload-slider',min=min_payload,max=max_payload,step=1000)),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart',figure= fig_scatter)),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):    
    
    if selected_site == "ALL":
        df = spacex_df
        title = "Launch Records for all sites"
        fig_pie = px.pie(df, values="class", names="Launch Site", title=title)        
        return fig_pie
    else:
        title = "Launch Records for "+selected_site
        df = spacex_df.loc[spacex_df['Launch Site'] == selected_site]   
        success_failure_df = df.groupby('class').size().reset_index(name='class count')
        colnames = ["result","count"]
        success_failure_df.columns = colnames
        col3 = []
        for index,row in success_failure_df.iterrows():
            if row["result"] == 0:
                col3.append("Failure")
            else:
                col3.append("Success")        
        success_failure_df["result text"] = col3
        fig_pie = px.pie(success_failure_df, values="count", names="result text", title=title)     
        return fig_pie
    



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='payload-slider', component_property='value'),
    Input(component_id='site-dropdown', component_property='value')]
)

def update_scatter_chart(slider_value, dropdown_value):
    #print(slider_value)
    #print(dropdown_value)
    min,max = slider_value
    if dropdown_value == "ALL":
        title = "Correlation between Payload and Success for all sites"
        df = spacex_df
        filter = (df['Payload Mass (kg)'] >= min) & (df['Payload Mass (kg)'] <= max)
        fig_scatter = px.scatter(df[filter], x='Payload Mass (kg)', y='class', color="Booster Version Category", title=title, range_y=[-0.2,1.2])
        return fig_scatter
    else:
        title = "Correlation between Payload and Success for "+dropdown_value
        df = spacex_df[spacex_df['Launch Site'] == dropdown_value]
        filter = (df['Payload Mass (kg)'] >= min) & (df['Payload Mass (kg)'] <= max)
        fig_scatter = px.scatter(df[filter], x='Payload Mass (kg)', y='class', color="Booster Version Category", title=title,range_y=[0.2,1.2])
        return fig_scatter
   

# Run the app
if __name__ == '__main__':
    app.run_server()
