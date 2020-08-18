import dash
import dash_core_components as dcc
import dash_html_components as html

from django_plotly_dash import DjangoDash
from plotly import graph_objs as go
from dash.exceptions import PreventUpdate
from django_pandas.io import read_frame
from backend.models import ARPwrPfCharts


app = DjangoDash('consumption_p')

app.layout = html.Div([
    dcc.Interval(
                id='my_interval',
                disabled=False,     #if True, the counter will no longer update
                interval=1*15000,    #increment the counter n_intervals every interval milliseconds
                n_intervals=0,      #number of times the interval has passed
                max_intervals=60,    #number of times the interval will be fired.
                                    #if -1, then the interval has no limit (the default)
                                    #and if 0 then the interval stops running.
    ),

    html.Div(id='output_data', style={'font-size':36}),
    dcc.Input(id="input_text",type='text'),
    dcc.Graph(id="mybarchart"),

])

#------------------------------------------------------------------------
@app.callback(
    [dash.dependencies.Output('output_data', 'children'),
     dash.dependencies.Output('mybarchart', 'figure')],
    [dash.dependencies.Input('my_interval', 'n_intervals')]
)
def update_graph(num):
    """update every 3 seconds"""
    if num==0:
        raise PreventUpdate
    else:
        y_data=num
        #line power and power factor
        data_power = ARPwrPfCharts.objects.using('energyst_pi').all()
        data_power = read_frame(data_power)
        data_power_m1 = data_power[data_power['Meter_Number']=='M0001']
        
        total_pwr_cur=round(float(data_power_m1.at[0,'TOTAL_PWR']),1)
        total_pwr_prev=round(float(data_power_m1.at[0,'TOTAL_PWR_PREV']),1)
        total_pf_cur=round(float(data_power_m1.at[0,'TOTAL_PF']),3)
        
        ph1_pwr_cur=round(float(data_power_m1.at[0,'PHASE1_PWR']),1)
        ph1_pwr_prev=round(float(data_power_m1.at[0,'PHASE1_PWR_PREV']),1)
        ph1_pf_cur=round(float(data_power_m1.at[0,'PHASE1_PF']),3)
        
        ph2_pwr_cur=round(float(data_power_m1.at[0,'PHASE2_PWR']),1)
        ph2_pwr_prev=round(float(data_power_m1.at[0,'PHASE2_PWR_PREV']),1)
        ph2_pf_cur=round(float(data_power_m1.at[0,'PHASE2_PF']),3)
        
        ph3_pwr_cur=round(float(data_power_m1.at[0,'PHASE3_PWR']),1)
        ph3_pwr_prev=round(float(data_power_m1.at[0,'PHASE3_PWR_PREV']),1)
        ph3_pf_cur=round(float(data_power_m1.at[0,'PHASE3_PF']),3)
        print('All')
        print(total_pwr_cur)
        print(total_pwr_prev)
        print(total_pf_cur)
        #
        #print('Phase1')
        #print(ph1_pwr_cur)
        #print(ph1_pwr_prev)
        #print(ph1_pf_cur)
        #
        #print('Phase3')
        #print(ph2_pwr_cur)
        #print(ph2_pwr_prev)
        #print(ph2_pf_cur)
        #print('Phase2')
        #print(ph3_pwr_cur)
        #print(ph3_pwr_prev)
        #print(ph3_pf_cur)
        total_pf_color = 'lightslategrey'
        if total_pf_cur <.85:
            total_pf_color = "red"
        elif total_pf_cur >=.85 and total_pf_cur <.95:
            total_pf_color = "yellow"
        else:
            total_pf_color = "yellowgreen"
            
        traces = []
        
        traces.append(go.Indicator(
                domain = {'x': [0.033, 0.533], 'y': [0.5, 1]},
                #value = float(data_power_m1.at[1,'TOTAL_PWR']),
                value = total_pf_cur,
                mode = "gauge",
                title = {'text': "Total", 'font': {'size': 16}},
                gauge = {
#                        'steps' : [
#                         {'range': [0, 1.0], 'color':"lightgray"},
#                         #{'range': [0.85, 0.95], 'color':"lightslategrey" },
#                         #{'range': [0.95, 1.0], 'color': "lightgrey"}
#                         ],
                     'axis': {'range': [0.8, 1.0]},
                     'bar': {'color': total_pf_color},
                         }
                                )
                        )
        
        traces.append(go.Indicator(
                mode = "number+delta",
            value = total_pwr_cur,
            number = {'suffix': "W"},
            delta = {"reference": total_pwr_prev, 'increasing': {'color': "Red"}, 'decreasing':{'color': "Green"},"valueformat": ".0f"},
            domain = {'x': [0.155, 0.405], 'y': [0.5, 0.75]}
            ))
        
        #phase 1
        traces.append(go.Indicator(
            domain = {'x': [0.0, 0.25], 'y': [0, 0.25]},
            value = ph1_pf_cur,
            mode = "gauge",
            title = {'text': "Phase1",'font': {'size': 14}},
            gauge = {
                     'steps' : [
                         {'range': [0, 0.85], 'color':"red"},
                         {'range': [0.85, 0.95], 'color':"yellow" },
                         {'range': [0.95, 1.0], 'color': "yellowgreen"}
                         ],
                     'axis': {'range': [0.0, 1.0]},
                     'bar': {'color': "grey"},
                     #'axis':{'visible': False},
                     #'threshold' : {'line': {'color': "red", 'width': 3}, 'thickness': 0.6, 'value': 0.8}
                    }
                    #domain = {'row': 0, 'column': 1}
                    ))
        
        traces.append(go.Indicator(
            mode = "number+delta",
            value = ph1_pwr_cur,
            number = {'suffix': "W"},
            delta = {"reference": ph1_pwr_prev,'increasing': {'color': "Red"}, 'decreasing':{'color': "Green"}, "valueformat": ".0f"},
            #title = {"text": "Current Energy Consumption"},
            domain = {'x': [0.058, 0.188], 'y': [0, 0.13]}
            ))
        
        
        #phase 2
        traces.append(go.Indicator(
            domain = {'x':[0.16, 0.41], 'y': [0, 0.25]},
            #'x': [0.0, 0.25], 'y': [0, 0.25]
            value = ph2_pf_cur,
            #mode = "gauge+number+delta",
            mode = "gauge",
            title = {'text': "Phase2",'font': {'size': 14}},
            gauge = {
                     'steps' : [
                         {'range': [0, 0.85], 'color':"red"},
                         {'range': [0.85, 0.95], 'color':"yellow" },
                         {'range': [0.95, 1.0], 'color': "yellowgreen"}
                         ],
                     'axis': {'range': [0.0, 1.0]},
                     'bar': {'color': "grey"},
                     #'axis':{'visible': False},
                     #'threshold' : {'line': {'color': "red", 'width': 3}, 'thickness': 0.6, 'value': 0.8}
                    }
                    #domain = {'row': 0, 'column': 1}
                    ))
        
        
        traces.append(go.Indicator(
            mode = "number+delta",
            value = ph2_pwr_cur,
            number = {'suffix': "W"},
            delta = {"reference": ph2_pwr_prev,'increasing': {'color': "Red"}, 'decreasing':{'color': "Green"}, "valueformat": ".0f"},
            #title = {"text": "Current Energy Consumption"},
            domain = {'x': [0.218, 0.348], 'y': [0, 0.13]}
            ))
        
        
        #phase 3
        traces.append(go.Indicator(
            domain = {'x':[0.32, 0.57], 'y': [0, 0.25]},
            value = ph3_pf_cur,
            #mode = "gauge+number+delta",
            mode = "gauge",
            title = {'text': "Phase3",'font': {'size': 14}},
            gauge = {
                     'steps' : [
                         {'range': [0, 0.85], 'color':"red"},
                         {'range': [0.85, 0.95], 'color':"yellow" },
                         {'range': [0.95, 1.0], 'color': "yellowgreen"}
                         ],
                     'axis': {'range': [0.0, 1.0]},
                     'bar': {'color': "grey"},
                     #'axis':{'visible': False},
                     #'threshold' : {'line': {'color': "red", 'width': 3}, 'thickness': 0.6, 'value': 0.8}
                    }
                    #domain = {'row': 0, 'column': 1}
                    ))
        
        
        traces.append(go.Indicator(
            mode = "number+delta",
            value = ph3_pwr_cur,
            number = {'suffix': "W"},
            delta = {"reference": ph3_pwr_prev,'increasing': {'color': "Red"}, 'decreasing':{'color': "Green"}, "valueformat": ".0f"},
            #title = {"text": "Current Energy Consumption"},
            domain = {'x': [0.378, 0.508], 'y': [0, 0.13]}
            ))
        
        
        
        fig = go.Figure(
                data = traces,
#                layout=go.Layout(
#                              title = 'Energy Consumption with Power Factor',
#                              xaxis = {'title':'Reading Date & Time'},
#                              yaxis = {'title':'Average Line Current'}
#                              )
               )


        fig.update_layout(
                            paper_bgcolor = "lavender", 
                            #autosize=False,
                            #width=500,
                            #height=500,
                            font = {
                                    'color': "darkblue", 
                                    'family': "monospace",
                                    'size':12
                                    },
        
                            title={
                                    'text': "Energy Consumption with Power Factor",
                                    'y':0.98,
                                    'x':0.31,
                                    'xanchor': 'center',
                                    'yanchor': 'top',
                                    'font': {
                                            "size": 28,
                                            "color": "darkblue",
                                            "family": "Arial"
                                            },
                                   }
                           
                         )
        
        
        
        #fig=go.Figure(data=[go.Bar(x=[1, 2, 3, 4, 5, 6, 7, 8, 9], y=[y_data]*9)],
         #             layout=go.Layout(yaxis=dict(tickfont=dict(size=22)))
        

    return (y_data,fig)

#data_line_current = pd.read_sql('SELECT * FROM `AR_LINE_CUR`', mycnx)
#data_line_current.set_index('ID',inplace=True)
#data_line_current = pd.read_csv('AR_LINE_CUR.csv')
#print (data_line_current.head())

#print(data_line_current.tail(5))
#list of columns I needed to be be together for the plot
#list_of_current_cols = ['Phase1_Current','Phase2_Current', 'Phase3_Current',  'Avg_Line_Current']




#x_values = data_line_current['cur_reading_time']
#for colname in list_of_current_cols:
#    #print (colname)
#    
#    y_values = data_line_current[colname]
#    traces.append(
#                  go.Scatter
#                      (
#                          x=x_values,
#                          y=y_values,
#                          mode='lines',
#                          name=colname
#                      )
#                 )


@app.callback(
    dash.dependencies.Output('my_interval', 'max_intervals'),
    [dash.dependencies.Input('input_text', 'value')]
)

def stop_interval(retrieved_text):
    if retrieved_text == 'stop':
        max_intervals = 0
    else:
        raise PreventUpdate

    return (max_intervals)
