# Jacob Ard
# CS-340 Project 2

from dash import Dash

# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc, html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64
#JupyterDash.infer_jupyter_proxy_config()

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from model.base import Base
from database import engine, SessionLocal
from model import Animal, AnimalType, Breed, OutcomeType, SexUponOutcome
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from dataclasses import dataclass, fields

###########################
# Data Manipulation / Model
###########################

Base.metadata.create_all(bind=engine)

# Connect to database via CRUD Module
db = SessionLocal()

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned

BASE_QUERY = select(Animal).options(
    joinedload(Animal.animal_type),
    joinedload(Animal.breed),
    joinedload(Animal.outcome_type),
    joinedload(Animal.sex_upon_outcome)
)
df = pd.read_sql(BASE_QUERY, con=engine)

DROP_COLS = ['animal_type_id',
             'breed_id', 'id', 'id_1', 'id_2', 'id_3', 'id_4',
             'outcome_type_id',
             'sex_upon_outcome_id']
# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
df.drop(columns=DROP_COLS,inplace=True)

## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)


#########################
# Dashboard Layout / View
#########################
app = Dash(__name__)

#FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
#FIX ME Also remember to include a unique identifier such as your name or date
#html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

#############################################
# Configuration Variables
# can be modified if preferred breed characteristics change
# ideally, these could be stored in a seperate .env file
#############################################

#FIX ME Add in Grazioso Salvare’s logo
IMAGE_FILENAME = 'Grazioso Salvare Logo.png' # replace with your own image
ENCODED_IMAGE = base64.b64encode(open(IMAGE_FILENAME, 'rb').read())

# url for image's anchor tag
HOME_PAGE_URL='https://www.snhu.edu'

# options for filter dropdown
FILTER_OPTIONS = [
    # label presented to user, value passed to update_dashboard callback
    {'label': 'Water Rescue', 'value': 'water-rescue'},
    {'label': 'Mountain Rescue', 'value': 'mountain-rescue'},
    {'label': 'Disaster Rescue', 'value': 'disaster-rescue'}
]

# options for chart dropdown
CHART_OPTIONS = [
    {'label': 'Pie Chart', 'value': 'pie'},
    {'label': 'Bar Chart', 'value': 'bar'}
]

# define the list of acceptable water rescue breeds
#### TODO: refactor breed, sex, and ages with an object-oriented approach ####
WATER_RESCUE_BREEDS = ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]
MOUNTAIN_RESCUE_BREEDS = ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]
# note: the dataset refers to the Doberman Pinscher as "Doberman Pinsch"
DISASTER_RESCUE_BREEDS = ["Doberman Pinsch", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]

# preferred sex upon outcome
WATER_RESCUE_SEX = "Intact Female"
MOUNTAIN_RESCUE_SEX = "Intact Male"
DISASTER_RESCUE_SEX = "Intact Male"

# min and max ages
WATER_RESCUE_MIN_AGE = 26
WATER_RESCUE_MAX_AGE = 156
MOUNTAIN_RESCUE_MIN_AGE = 26
MOUNTAIN_RESCUE_MAX_AGE = 156
DISASTER_RESCUE_MIN_AGE = 20
DISASTER_RESCUE_MAX_AGE = 300

app.layout = html.Div([
    html.Div(
        [
            # wrap image in anchor tag
            html.A(
                html.Img(
                    src='data:image/png;base64,{}'.format(ENCODED_IMAGE.decode()),
                    # reduce the size of the image
                    style={'height': '25%', 'width': '25%'}
                ), 
                href=HOME_PAGE_URL, # link to snhu site
                target='_blank', # open in new tab
                rel='noopener noreferrer',
                # use flexbox to align image to the left 
                style={
                    'flex': '1', 
                    'text-align': 'left'
                }
            ),
            # App title
            html.B(html.H1('Austin Animal Centers'), style={'flex': '1', 'text-align': 'center'}),
            # display unique identifier (my name) on the right
            html.H2('Jacob Ard', id='unique-identifier', style={'flex': '1', 'text-align': 'right'}),
        ],
        style={
            'display': 'flex', 
            'flex-direction': 'row', 
            'justify-content': 'space-between',
            'align-items': 'center'
        }
    ),
    
    html.Hr(),
    html.Div(),
    html.Div([
        dcc.Dropdown(
            id='filter-type',
            options=FILTER_OPTIONS,
            placeholder='Select Rescue Type...',
            # could leave this as true to allow reset by clicking the small 'x' button
            # instead, I made an external reset button with a callback
            clearable=False,
            style={'width': '200px'}
        ),
        html.Button('Reset', id='reset-btn', n_clicks=0, style={'marginLeft': '10px'})
    ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center'}),
    html.Hr(),
    dash_table.DataTable(
        id='datatable-id',               
        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in sorted(df.columns)],
        data=df.to_dict('records'),
        # enable single row selection
        row_selectable='single',
        # native pagination w/ 10 records per page
        page_action='native',
        page_current=0,
        page_size=10,
        # native sorting by multiple columns 
        sort_action='native',
        sort_mode='multi',
        # allow user to select multiple columns
        column_selectable='multi',
        # select first row to avoid issues w/ geolocation chart
        selected_rows=[0]

    ),
    html.Br(),
    html.Hr(),
    
    html.Div(
        # drop down for switching between pie chart and histogram
        dcc.Dropdown(
            id='chart-type', 
            value='pie', 
            options=CHART_OPTIONS,
            clearable=False,
            style={'width': '200px'}
        )
    ),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################



    
@app.callback([Output('datatable-id','data'),
              Output('datatable-id', 'selected_rows')],
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    # filter by water rescue
    if filter_type == 'water-rescue':
        query_where = (BASE_QUERY
        # Join related tables
        .join(Animal.animal_type)
        .join(Animal.breed)
        .join(Animal.sex_upon_outcome)
        .join(Animal.outcome_type)
        .where(
            # where breed in Lab Ret, Chesapeke Bay, Newfoundland
            Animal.breed.has(
                Breed.breed_name
                .in_(WATER_RESCUE_BREEDS)),
            # And AGE between 26 & 156 weeks
            Animal.age_upon_outcome_in_weeks >= WATER_RESCUE_MIN_AGE,
            Animal.age_upon_outcome_in_weeks <= WATER_RESCUE_MAX_AGE,
            # And sex is Intact Female
            Animal.sex_upon_outcome.has(
                SexUponOutcome.sex == WATER_RESCUE_SEX
            )
        ))

    elif filter_type == 'mountain-rescue':
        query_where = (BASE_QUERY
        .join(Animal.animal_type)
        .join(Animal.breed)
        .join(Animal.sex_upon_outcome)
        .join(Animal.outcome_type)
        .where(
            # Where breed is german shep, alaskan malamute, old eng. sheepdog, husky, rottweiler
            Animal.breed.has(
                Breed.breed_name
                .in_(MOUNTAIN_RESCUE_BREEDS)),
            # and age between 26 & 156 weeks
            Animal.age_upon_outcome_in_weeks >= MOUNTAIN_RESCUE_MIN_AGE,
            Animal.age_upon_outcome_in_weeks <= MOUNTAIN_RESCUE_MAX_AGE,
            # and sex is Intact Male
            Animal.sex_upon_outcome.has(
                SexUponOutcome.sex == MOUNTAIN_RESCUE_SEX
            )
        ))
    # filter disaster rescue
    elif filter_type == 'disaster-rescue':
        query_where = (BASE_QUERY
        .join(Animal.animal_type)
        .join(Animal.breed)
        .join(Animal.sex_upon_outcome)
        .join(Animal.outcome_type)
        .where(
            # where breed is dobermann, g. shepard, gold ret., bloodhound, rottweiler
            Animal.breed.has(
                Breed.breed_name
                .in_(DISASTER_RESCUE_BREEDS)),
            # and age between 20 & 300 weeks
            Animal.age_upon_outcome_in_weeks >= DISASTER_RESCUE_MIN_AGE,
            Animal.age_upon_outcome_in_weeks <= DISASTER_RESCUE_MAX_AGE,
            # andsex is intact male
            Animal.sex_upon_outcome.has(
                SexUponOutcome.sex == DISASTER_RESCUE_SEX
            )
        ))
    else:
        # else use base query
        query_where = BASE_QUERY

    # pass sql statement with filters to db.scalars method to return list of Animals
    #data = pd.DataFrame.from_records(db.scalars(query_where).all())
    data = pd.read_sql(query_where, con=engine)
    # drop _id column to prevent data table crash
    data.drop(columns=DROP_COLS,inplace=True)


    # return the datatable's new data
    # return selected_index[0] to avoid an Index out of range error
    return data.to_dict('records'), [0]


# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
    Input('chart-type', "value")])
def update_graphs(view_data, chart_type):
    # return empty list if there's no derived_virtual_data
    if view_data is None:
        return []
    
    if chart_type == 'pie':
        pie_chart = create_pie_chart(view_data)
        
        return [
            dcc.Graph(
                figure = pie_chart
            )
        ]
    else:
        bar_chart = create_bar_chart(view_data)

        return [
           dcc.Graph(            
               figure = bar_chart
           )    
        ]

# creates and returns a plotly pie chart figure
def create_pie_chart(data):
    pie_chart = px.pie(data, names='breed_name', title='Animals by Breed')
    pie_chart.update_traces(
        # display breed name, count and percentage on hover
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}",
        # display text inside the chart
        textposition='inside'
    )
    # hide text labels if they don't fit within a slice
    pie_chart.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
    
    return pie_chart

# creates and returns a plotly bar chart (histogram)
def create_bar_chart(data):
    # create horizontal bar chart w/ breed on the y-axis
    # text_auto adds text labels to the histogram's bars
    bar_chart = px.histogram(data, y='breed_name', title='Animals by Breed', text_auto=True)
    # set x-axis title, display only discrete values 
    bar_chart.update_xaxes(title="Count", tickformat="d")
    # set y-axis title
    bar_chart.update_yaxes(title="Breed")
    
    return bar_chart
    
#This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    # return empty list if no columns are selected
    if selected_columns is None:
        return []
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")],
    # prevents the callback from immediately firing on refresh, which was causing an error
    prevent_initial_call=True)
def update_map(view_data, index):  
    if view_data is None:
        return
    elif index is None:
        return
    
    dff = pd.DataFrame.from_dict(view_data)
    # Because we only allow single row selection, the list can be converted to a row index here
    if index is None:
        row = 0
    else: 
        row = index[0]
        
    # set lat/long variable to center the map and set marker position
    latitude=dff.iloc[row, 8]
    longitude=dff.iloc[row,9]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[latitude,longitude], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            # Column 13 and 14 define the grid-coordinates for the map
            # Column 4 defines the breed for the animal
            # Column 9 defines the name of the animal
            dl.Marker(position=[latitude, longitude], children=[
                dl.Tooltip(dff.iloc[row,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[row,9])
                ])
            ])
        ])
    ]

# callback for external dropdown reset button
@app.callback(
    Output('filter-type', 'value'),
    Input('reset-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_dropdown_menu(n_clicks):
    # return None to clear the select 
    # and revert to unfiltered list
    return None

# Run app and display result in jupyterlab mode, note, if you have previously run a prior app, the default port of 8050 may not be available, if so, try setting an alternate port.
#app.run_server() 
if __name__ == "__main__":
    app.run(debug=True)
