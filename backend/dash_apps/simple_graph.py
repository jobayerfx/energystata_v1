import dash
import dash_core_components as dcc
import dash_html_components as html

from django_plotly_dash import DjangoDash
from plotly import graph_objs as go
import plotly.express as px
from django_pandas.io import read_frame
from backend.models import ARSynesisitDB1

#line Current
qs = ARSynesisitDB1.objects.using('energyst_pi').all()
# data_raw = qs.to_dataframe()
# data_raw .set_index('id',inplace=True)
data_line_current = read_frame(qs, fieldnames=['Meter_Number','Phase','reading_dt','YR','MTH', 'WK', 'Weekday', 'cur_reading_time','Line_Current'])
most_recent_reading_tf = ARSynesisitDB1.objects.using('energyst_pi').latest('reading_dt').reading_dt
# most_recent_yr= data_line_current[data_line_current['reading_dt']==most_recent_reading_tf]['YR'].unique()[0]
most_recent_yr= ARSynesisitDB1.objects.using('energyst_pi').latest('reading_dt').reading_dt.year
#print(most_recent_yr)
most_recent_wk=data_line_current[data_line_current['reading_dt']==most_recent_reading_tf]['WK'].unique()[0]
#print(most_recent_wk)
#data_line_cur_today = data_line_current[(data_line_current['YR']==most_recent_yr) 
#                                      & (data_line_current['WK']==most_recent_wk)]
most_recent_update = data_line_current['cur_reading_time'].max()
data_line_cur_today = data_line_current[(data_line_current['reading_dt']==most_recent_reading_tf)]


app = DjangoDash('SimpleExample')

app.layout = html.Div(
                        [
                          
                          html.Div(
                                   [
                                     html.Br(),
                                     html.Label(['Select a Meter no:'],style={'font-weight': 'bold', "text-align": "center"}),
                                     
                                     dcc.Dropdown(id='meter_no',
                                        options=[{'label':x, 'value':x} for x in data_line_cur_today.sort_values('Meter_Number')['Meter_Number'].unique()],
                                        value='M0001',
                                        multi=False,
                                        disabled=False,
                                        clearable=True,
                                        searchable=True,
                                        placeholder='Choose Meter...',
                                        className='form-dropdown',
                                        style={'width':"50%"},
                                        persistence='string',
                                        persistence_type='memory'),
                                    html.Label([' '],style={'font-weight': 'bold', "text-align": "center"}),                                                                        
                                    html.Label(['Choose the lines you want to compare:'],style={'font-weight': 'bold', "text-align": "center"}),                                    
                                   
                                    dcc.Dropdown(id='line1',
                                        options=[{'label':x, 'value':x} for x in data_line_cur_today.sort_values('Phase')['Phase'].unique()],
                                        value='Total',
                                        multi=False,
                                        disabled=False,
                                        clearable=True,
                                        searchable=True,
                                        placeholder='Choose Line1...',
                                        className='form-dropdown',
                                        style={'width':"50%"},
                                        persistence='string',
                                        persistence_type='memory'),
                            
                                    
                                    dcc.Dropdown(id='line2',
                                        options=[{'label':x, 'value':x} for x in data_line_cur_today.sort_values('Phase')['Phase'].unique()],
                                        value='Phase1',
                                        multi=False,
                                        disabled=False,
                                        clearable=True,
                                        searchable=True,
                                        placeholder='Choose Line2...',
                                        className='form-dropdown',
                                        style={'width':"50%"},
                                        persistence='string',
                                        persistence_type='memory'),
                                   
                                   html.Label(['-------------------------------------------------- '],style={'font-weight': 'bold', "text-align": "center"}),                          
                                   html.Label(['Last updated at '+ most_recent_update],style={'font-weight': 'bold', "text-align": "center"}),
                                   html.Label([' --------------------------------------------------'],style={'font-weight': 'bold', "text-align": "center"}),
                                  ],className='three columns'
                                  ), 
                         html.Div(
                                   [
                                     dcc.Graph(id='our_graph')
                                   ],className='nine columns'
                                  ),
                        ]
                     )

@app.callback(
                dash.dependencies.Output('our_graph','figure'),
                [
                    dash.dependencies.Input('meter_no','value'),
                    dash.dependencies.Input('line1','value'),
                    dash.dependencies.Input('line2','value')
                ]
             )


def update_graph(meterno,line1,line2):
    #data only for selected phase
    df_line_cur = data_line_cur_today[(data_line_cur_today['Meter_Number']== meterno)]
    df_line_cur1 = df_line_cur[
                                (df_line_cur['Phase']==line1)|
                                (df_line_cur['Phase']==line2)
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