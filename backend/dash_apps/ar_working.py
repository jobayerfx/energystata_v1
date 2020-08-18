#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 20:34:01 2020

@author: ardodul
"""

# import and graph setup
import dash
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go

#libraries for mysql connection
from sqlalchemy import create_engine
import pymysql
#import other libraries
from datetime import datetime
import pandas as pd
import plotly.express as px
from django_pandas.io import read_frame
from backend.models import ARSynesisitDB1

#create dataframe

#line Current
qs = ARSynesisitDB1.objects.using('energyst_pi').all()

data_line_current = read_frame(qs, fieldnames=['Meter_Number','Phase','reading_dt','YR','MTH', 'WK', 'Weekday', 'cur_reading_time','Line_Current'])

# most_recent_reading_tf = data_line_current['reading_dt'].max()
# most_recent_yr= data_line_current[data_line_current['reading_dt']==most_recent_reading_tf]['YR'].unique()[0]
most_recent_reading_tf = ARSynesisitDB1.objects.using('energyst_pi').latest('reading_dt').reading_dt
most_recent_yr= ARSynesisitDB1.objects.using('energyst_pi').latest('reading_dt').reading_dt.year
#print(most_recent_yr)
most_recent_wk= data_line_current[data_line_current['reading_dt']==most_recent_reading_tf]['WK'].unique()[0]
#print(most_recent_wk)

most_recent_update = data_line_current['cur_reading_time'].max()
data_line_cur_today = data_line_current[(data_line_current['reading_dt']==most_recent_reading_tf)]


app= DjangoDash('arworking_p')


app.layout = html.Div(
                        [ #main Div start
                        #"This is the main div",
                        html.Div(
                                    [#main-1 Div start
                                    #"This is the main-1 div"
                                    html.H1(
                                            html.Label("Line Current Comparison Chart")
                                           ),
                                    ],#main-1 Div end
                                    style = {#main-1 Div
                                                       'color':'white',
                                                       'font-family': 'Courier New',
                                                       'text-align': 'center',
                                                       'height': '41px',
                                                       'width': '99.9%',
                                                       #'outline': '3px solid blue',
                                                       'background-image': 'linear-gradient(to bottom right,darkturquoise,aquamarine )'
                                                        
                                                        
                                           }
                                ),
                        html.Hr(), #creates a horizontal line between Divs
             
                        html.Div(
                                    [#main-2 Div start
                                    #"This is the main-1 div"
#                                    html.Hr(), #creates a horizontal line between Divs
                                    
                                    html.Div(
                                            [
                                            html.Label(['-----'],style={'font-weight': 'bold', "text-align": "center"}),                          
                                            html.Label(['Last updated at '+ most_recent_update],style={'font-family': 'Courier New','font-size': '20px','font-weight': 'bold', "text-align": "center",}),
                                            html.Label(['------'],style={'font-weight': 'bold', "text-align": "center"})
                                            ],
                                            style = {#main-2-1 Div
                                                       'color':'white',
                                                       'text-align': 'center',
                                                       'font-family': 'Courier New',
                                                       'width': '99.2%',
                                                       'padding':5
                                                      
                                                     }
                                            ),
                                    html.Hr(), #creates a horizontal line between Divs
                                    
                                    html.Div(
                                                [#main-2-1 Div start
                                                    html.Label(['Select a Meter no:'],style={'font-size': '20px','font-weight': 'bold', "text-align": "center"}),
                                                    html.Hr(), #creates a horizontal line between Divs
                                                    dcc.Dropdown(id='meter_no',
                                                                 options=[
                                                                         #{'label':x, 'value':x} for x in ['M0001','M0002','M0003']],
                                                                         {'label':x, 'value':x} for x in data_line_cur_today.sort_values('Meter_Number')['Meter_Number'].unique()],                             
                                                                 value='M0001',
                                                                 multi=False,
                                                                 disabled=False,
                                                                 clearable=True,
                                                                 searchable=True,
                                                                 placeholder='Choose Meter...',
                                                                 className='form-dropdown',
                                                                 style={#'width':"25%",
                                                                        'color':'black',
                                                                        'font-family': 'Courier New'
                                                                         },
                                                                 persistence='string',
                                                                 persistence_type='memory')
                                                ],#main-2-1 Div end
                                            
                                                style = {#main-2-1 Div
                                                           'color':'white',
                                                           'font-family': 'Courier New',
                                                           'text-align': 'left',
                                                           'background-image': 'linear-gradient(to bottom ,darkturquoise,aquamarine )',
                                                           'display':'inline-block',
                                                           'height': '90px',
                                                           'width': '23.5%',

                                                           'padding':5
                                                          },
                                                
                                            ),
                                    
                                    

                                    html.Div(
                                                [#main-2-2 Div start
                                                        html.Label(['Select Line:'],style={'font-size': '20px','font-weight': 'bold', "text-align": "center"}),
                                                        html.Hr(), #creates a horizontal line between Divs
                                                        dcc.Dropdown(id='line1',
                                                        options=[
                                                                {'label':x, 'value':x} for x in data_line_cur_today.sort_values('Phase')['Phase'].unique()
                                                                ],
                                                        value='Phase1',
                                                        multi=False,
                                                        disabled=False,
                                                        clearable=True,
                                                        searchable=True,
                                                        placeholder='Choose Line1...',
                                                        className='form-dropdown',
                                                        style={
                                                               'color':'black',
                                                               'font-family': 'Courier New'
                                                              },
                                                        persistence='string',
                                                        persistence_type='memory'), 
                                                ],#main-2-2 Div end
                                            
                                                style = {#main-2-1 Div
                                                       'color':'white',
                                                       'font-family': 'Courier New',
                                                       'background-color':'white',
                                                       'text-align': 'left',
                                                       'background-image': 'linear-gradient(to bottom ,darkturquoise,aquamarine )',
                                                       'display':'inline-block',
                                                       'height': '90px',
                                                       'width': '23.5%',
                                                       'padding':5
                                                      
                                                      },
                                                
                                            ),

                                    html.Div(
                                                [#main-2-3 Div start
                                                        html.Label(['Select Line:'],style={'font-size': '20px','font-weight': 'bold', "text-align": "center"}),
                                                        html.Hr(), #creates a horizontal line between Divs
                                                        dcc.Dropdown(id='line2',
                                                        options=[
                                                                {'label':x, 'value':x} for x in data_line_cur_today.sort_values('Phase')['Phase'].unique()],
                                                                value='Phase2',
                                                                multi=False,
                                                                disabled=False,
                                                                clearable=True,
                                                                searchable=True,
                                                                placeholder='Choose Line2...',
                                                                className='form-dropdown',
                                                                style={#'width':"25%"
                                                                       'color':'black',
                                                                       #'display': "inline-block"
                                                                       'font-family': 'Courier New'
                                                                      },
                                                                persistence='string',
                                                                persistence_type='memory') 
                                                ],#main-2-3 Div end
                                            
                                                style = {#main-2-1 Div
                                                       'color':'white',
                                                       'font-family': 'Courier New',
                                                       'background-color':'darkturquoise',
                                                       'text-align': 'left',
                                                       'background-image': 'linear-gradient(to bottom ,darkturquoise,aquamarine )',
                                                       'display':'inline-block',
                                                       'height': '90px',
                                                       'width': '23.5%',
                                                       'padding':5
                                                      },
                                                
                                            ),
                                    html.Div(
                                                [#main-2-4 Div start
                                                        html.Label(['Select Line:'],style={'font-size': '20px','font-weight': 'bold', "text-align": "center"}),
                                                        html.Hr(), #creates a horizontal line between Divs
                                                        dcc.Dropdown(id='line3',
                                                        options= [
                                                                {'label':x, 'value':x} for x in data_line_cur_today.sort_values('Phase')['Phase'].unique()],
                                                                value='Phase3',
                                                                multi=False,
                                                                disabled=False,
                                                                clearable=True,
                                                                searchable=True,
                                                                placeholder='Choose Line3...',
                                                                className='form-dropdown',
                                                                style={#'width':"25%"
                                                                       'color':'black',
                                                                       #'display': "inline-block"
                                                                       'font-family': 'Courier New'
                                                                      },
                                                                persistence='string',
                                                                persistence_type='memory') 
                                                ],#main-2-3 Div end
                                            
                                                style = {#main-2-1 Div
                                                       'color':'white',
                                                       'font-family': 'Courier New',
                                                       'background-color':'darkturquoise',
                                                       'text-align': 'left',
                                                       'background-image': 'linear-gradient(to bottom ,darkturquoise,aquamarine )',
                                                       'display':'inline-block',
                                                       'height': '90px',
                                                       'width': '23.5%',
                                                       'padding':5
                                                      },
                                                
                                            ),

                                    ],#main-1 Div end
                                    style = {#main-1 Div
                                                       'color':'white',
                                                       'text-align': 'center',
                                                       'font-family': 'Courier New',                                                       
                                                       'height': '150px'                                                                                                                
                                           }
                                ),
                      html.Hr(), #creates a horizontal line between Divs
             
                      html.Div(
                                    [#main-1 Div start
                                    #"This is the main-1 div"
                                    dcc.Graph(id='our_graph')
                                    
                                    ],#main-1 Div end
                                    style = {#main-1 Div
                                                       'color':'white',
                                                       'text-align': 'center',
                                                       'background-image': 'linear-gradient(to bottom right,darkturquoise,aquamarine )'
                                                        
                                                        
                                           }
                                )              
                      ],#main Div end
                      style = {#main Div
                                  'font-family': 'Courier New',
                                  'background-color':'lightblue',
                                  'padding':5
                                
                              }
                         
                     )
        
        #--------------------------------------------------------------
        
        
#                        [
#                          html.Div(
#                                   [
#                                     html.Br(),
#                                     html.Label(['Select a Meter no:-------------------------------------Choose the lines you want to compare:'],style={'font-weight': 'bold', "text-align": "center"}),
#                                     #html.Label(['  '],style={'font-weight': 'bold', "text-align": "center"}),                                                                        
#                                     #html.Label(['Choose the lines you want to compare:'],style={'font-weight': 'bold', "text-align": "center"})                                    
#                                    ]
#                                   ),
#                          html.Div(
#                                   [
#                                     html.Br(),
#                                     #html.Label(['Select a Meter no:'],style={'font-weight': 'bold', "text-align": "center"}),
#                                     
#                                     dcc.Dropdown(id='meter_no',
#                                        options=[{'label':x, 'value':x} for x in data_line_cur_today.sort_values('Meter_Number')['Meter_Number'].unique()],
#                                        value='M0001',
#                                        multi=False,
#                                        disabled=False,
#                                        clearable=True,
#                                        searchable=True,
#                                        placeholder='Choose Meter...',
#                                        className='form-dropdown',
#                                        style={'width':"25%",
#                                               'display': "inline-block"},
#                                        persistence='string',
#                                        persistence_type='memory'),
#                                    #html.Label([' '],style={'font-weight': 'bold', "text-align": "center"}),                                                                        
#                                    #html.Label(['Choose the lines you want to compare:'],style={'font-weight': 'bold', "text-align": "center"}),                                    
#                                   
#                                    dcc.Dropdown(id='line1',
#                                        options=[{'label':x, 'value':x} for x in data_line_cur_today.sort_values('Phase')['Phase'].unique()],
#                                        value='Total',
#                                        multi=False,
#                                        disabled=False,
#                                        clearable=True,
#                                        searchable=True,
#                                        placeholder='Choose Line1...',
#                                        className='form-dropdown',
#                                        style={'width':"25%",
#                                               'display': "inline-block"},
#                                        persistence='string',
#                                        persistence_type='memory'),
#                            
#                                    
#                                    dcc.Dropdown(id='line2',
#                                        options=[{'label':x, 'value':x} for x in data_line_cur_today.sort_values('Phase')['Phase'].unique()],
#                                        value='Phase1',
#                                        multi=False,
#                                        disabled=False,
#                                        clearable=True,
#                                        searchable=True,
#                                        placeholder='Choose Line2...',
#                                        className='form-dropdown',
#                                        style={'width':"25%",
#                                               'display': "inline-block"},
#                                        persistence='string',
#                                        persistence_type='memory'),
#                                   
#                                   html.Label(['------------------------------------------------------------------------------------------'],style={'font-weight': 'bold', "text-align": "center"}),                          
#                                   html.Label(['Last updated at '+ most_recent_update],style={'font-weight': 'bold', "text-align": "center"}),
#                                   html.Label(['--------------------------------------------------------------------------------'],style={'font-weight': 'bold', "text-align": "center"}),
#                                  ],className='three columns'
#                                  ), 
#                         html.Div(
#                                   [
#                                     dcc.Graph(id='our_graph')
#                                   ],className='nine columns'
#                                  ),
#                        ]
#                     )
#
@app.callback(
                Output('our_graph','figure'),
                [
                    Input('meter_no','value'),
                    Input('line1','value'),
                    Input('line2','value'),
                    Input('line3','value')
                ]
             )
#
#
def update_graph(meterno,line1,line2,line3):
    #data only for selected phase
    df_line_cur = data_line_cur_today[(data_line_cur_today['Meter_Number']== meterno)]
    df_line_cur1 = df_line_cur[
                                (df_line_cur['Phase']==line1)|
                                (df_line_cur['Phase']==line2)|
                                (df_line_cur['Phase']==line3)
                              ]
    #print (df_line_cur1.head(5))    
    
    linecurrent_chart = px.line(
                                df_line_cur1, 
                                x="cur_reading_time", y="Line_Current", color='Phase',height = 600)
                                
    
    linecurrent_chart.update_layout(
                                        yaxis={'title':'Current(amp)'},
                                        title={'text':'Line Current Comparison Chart',
                                        'font':{'size':28},'x':0.5,'xanchor':'center'}
                                    )
    return (linecurrent_chart)


    
if __name__=='__main__':
    app.run_server()  

