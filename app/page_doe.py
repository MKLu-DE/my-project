from dash import html
from dash_components import *
from app import app
# from models.model_functions import GAB_T, run_simulation
from dash.dependencies import Input, Output, State
import numpy as np 
import plotly.graph_objects as go




layout = html.Div([

    row_with_columns(
        columnContents=[
            # column1
            card(
                cardHeader="Experimental Conditions",
                content=[

                    html.Section('- Equilibrium Seed Moisture', style=html_section_style),

                    label_input_number(labelName="Storage RH [%]",  
                                        defaultInputValue=30.0, inputID="RH_doe"),
                    label_input_number(labelName="Storage T [°C]",  defaultInputValue=8.0, inputID="T_doe"),
                    label_input_number(labelName="Equilibrium Seed Moisture [d.b. %]", inputID="Meq_doe", disabled=True),
                    
                    html.Section('- Requirements', style=html_section_style),

                    label_input_number(labelName="Batch size (g)",  
                                        defaultInputValue=300.0, inputID="batch_size_doe"),

                    dropdownMenu(dropdownName="Drum type", dropdownID="select_drum_doe", 
                                 options=[
                                        {'label': 'small', 'value': 'small'},
                                        {'label': 'large', 'value': 'large'},],
                    ),

                    label_input_number(labelName="Inlet air velocity [m/s]",   
                                       defaultInputValue=1.3, inputID="air_velocity_in_doe"),
                    label_input_number(labelName="Outlet air velocity [m/s]",   
                                       defaultInputValue=1.1, inputID="air_velocity_out_doe"),
                    
                    html.Section('- DoE Variables', style=html_section_style),
                    label_input_number(labelName="Initial moisture [d.b.%]",  
                                       defaultInputValue=75.0, inputID="init_M_doe"),

                    label_input_number(labelName="Drying temperature [°C]",  
                                       defaultInputValue=12.0, inputID="drying_T_doe"), 
                    
                    label_input_number(labelName="Drying RH [%]",  
                                       defaultInputValue=37.0, inputID="drying_RH_doe"), 


                    html.Section('- Simulation Conditions', style=html_section_style),
                    label_input_number(labelName="Drying factor [-]",  
                                       defaultInputValue=12.0, inputID="drying_factor_doe", disabled=True),

                    label_input_number(labelName="Hole size [mm]",  
                                       defaultInputValue=30.0, 
                                       stepValue=1.0, inputID="hole_size_doe",
                                       style_label={'fontWeight':'bold', 'color':'blue'},
                                       style_box={'width':"100%", 'textAlign':'center', 'fontWeight':'bold', 'color':'blue'}),

                    label_input_number(labelName="Targeted end point [days]",  
                                       defaultInputValue=2.5, 
                                       stepValue=0.1, inputID="end_day_doe",
                                       style_label={'fontWeight':'bold', 'color':'blue'},
                                       style_box={'width':"100%", 'textAlign':'center', 'fontWeight':'bold', 'color':'blue'}),

                    label_input_number(labelName="Threshold: moisture gap [d.b.%]",  
                                       defaultInputValue=0.8, 
                                       stepValue=0.1, inputID="mois_diff_doe",
                                       style_label={'fontWeight':'bold', 'color':'blue'},
                                       style_box={'width':"100%", 'textAlign':'center', 'fontWeight':'bold', 'color':'blue'}),

                    button(buttonName="Run Simulation", buttonID="run_doe", buttonColor="green"),
                ]
            ),
            # column2
            card(
                cardHeader="Simulation Results",
                content=[
                    html.Div(id="simulation_report", style={'margin-left':'20px', 'margin-right':'20px'}),
                    html.Div(id="plot_results_doe", style={'margin-left':'20px', 'margin-right':'20px'})
                ]
            ),
        ],
        columnWidth=[4, 8]
    ), 

    html.Div(id="get_Meq_alert_doe"),
    html.Div(id="run_doe_alert"),
    
])

# default drum type 

@app.callback(
        Output('select_drum_doe', 'value'),
        [
            Input("batch_size_doe", "value")
        ]
)
def drum_type(batch_size_doe):

    if batch_size_doe >= 400.0:
        return "large"
    else:
        return "small"

""" 
# ---------------------------------- Meq ----------------------------------
@app.callback(
    [
        Output('Meq_doe', 'value'),
        Output('get_Meq_alert_doe', 'children'),
    ],
    [
        Input('RH_doe', 'value'),
        Input('T_doe', 'value'),
    ],
)
def GetMeq(RH, T):
    if RH < 0 or RH > 100:
        notice = dbc.Toast(
                        "RH value should be >= 0 and <= 100.", header="Estimation failed", 
                        icon="danger", duration=7000, 
                        style=notification_style,
                    )
        return "Wrong", notice
    else:
        return str(round(GAB_T(RH/100, T) * 100, 2)), []





# get outlet air velocity and drying factor based on selected drum type
@app.callback(
    [
        Output('air_velocity_out_doe', 'value'),
        Output('drying_factor_doe', 'value'),
    ],
    [
        Input('select_drum_doe', 'value'),
    ],
)
def get_us_drying_factor(drum_type):

    if drum_type == "small":
        return 1.1, 16.2
    else:
        return 0.9, 11.8
    


# run GSA 
@app.callback(
    [   Output('run_doe_alert', 'children'),
        Output("simulation_report", "children"),
        # drum
        Output("plot_results_doe", "children"),
    ],
    [
        Input('run_doe', 'n_clicks'),
    ],
    [
        State('batch_size_doe', 'value'),
        State('select_drum_doe', 'value'),
        State('air_velocity_in_doe', 'value'),
        State('air_velocity_out_doe', 'value'),
        # State('doe_table', 'derived_virtual_data'),
        State('init_M_doe', 'value'),
        State('drying_T_doe', 'value'),
        State('drying_RH_doe', 'value'),
        State('drying_factor_doe', 'value'),
        State('hole_size_doe', 'value'),
        State("end_day_doe", "value"),
        State('mois_diff_doe', 'value')
    ],
)
def run_doe(click, batch_size_doe, select_drum_doe,
        air_velocity_in_doe, air_velocity_out_doe, 
        # doe_table_data, 
        init_M_doe, drying_T_doe, drying_RH_doe,
        drying_factor_doe, hole_size_doe, end_day_doe, mois_diff_doe): 
    
    if click == 0:
        return [], [], []
    else:
        check_list = [batch_size_doe, select_drum_doe,
            air_velocity_in_doe, air_velocity_out_doe, 
            init_M_doe, drying_T_doe, drying_RH_doe, 
            drying_factor_doe, hole_size_doe, end_day_doe, mois_diff_doe]
        
        for i in check_list:
            if i == None or []:
                notice = dbc.Toast(
                        "Missing data!", 
                        header="Failed",
                        icon="danger",
                        duration=7000,
                        style=notification_style,
                    )
                return notice, [], []

        # moisture diffucivity, m2/s
        De                      = 1e-3
        # heat diffucivity, W/m/K
        k_cond                  = -0.01
        # heat transfer factor
        ht_factor               = 0.20
        # critical moisture
        M_cr                    = 0.25
        # order of reynolds number
        a1                      = 1/5
        # order of temperature effect
        a2                      = 0.0

        mass_dry_seed_init      = batch_size_doe/ 1000 / (1 + 0.1022)

        time_array      = np.array([0.0, (end_day_doe + 3) * 24 * 3600.0])
        Troom_array     = np.array([drying_T_doe, drying_T_doe])
        RH_room_array   = np.array([drying_RH_doe, drying_RH_doe])/100.0
        Meq_doe         = GAB_T(drying_RH_doe/100.0, drying_T_doe)
         
        title = f"* Hole size: {hole_size_doe} mm"
        
        solution                = run_simulation(time_array, Troom_array, RH_room_array, 
                                                    air_velocity_in_doe, air_velocity_out_doe,
                                                    init_M_doe/100, mass_dry_seed_init, M_cr,
                                                    select_drum_doe, hole_size_doe/1000,  
                                                    ht_factor, k_cond, De, 
                                                    a1, a2, drying_factor_doe)
        
        time_day, M_sol, y_air_sol, T_seed_sol, T_air_sol = solution

        M_25                    = np.interp(end_day_doe, time_day, M_sol[0])
        title += f" | Seed moisture at {end_day_doe} days: {round(M_25*100, 2)} % | Equilibrium seed moisture {round(Meq_doe*100,2)} %"

        dM_dt = -np.diff(M_sol[0]*100) / (time_day[1]-time_day[0])

        pred_plot = go.Figure()
        pred_plot.add_trace(go.Scatter(x= time_day, y= M_sol[0]*100, mode='lines', 
                                       line=dict(color="black"),
                                       name= "Prediction"))
        
        
        pred_plot.add_trace(go.Scatter(x= time_day, y= [Meq_doe*100 for _ in range(len(time_day))], mode='lines', 
                                       line=dict(color="green"),
                                       name= "Equilibrium"))

        pred_plot.update_layout(
                            # title_text=title,
                            xaxis_title='time (days)', 
                            yaxis_title='Seed Moisture (d.b. %)', 
                            xaxis=dict(tick0=0, dtick=0.5),
                            xaxis_range=[0, time_day[-1]],
                            yaxis_range=[0, 90],
                            legend=dict(orientation='h', 
                                        yanchor='top', 
                                        y=1.12
                                        ))
        
        M_change_plot = go.Figure()
        M_change_plot.add_trace(go.Scatter(x= time_day[:-1], y= dM_dt, mode='lines', 
                                       line=dict(color="black"),
                                       name= "Seed Moisture Gradient"))
        
        M_change_plot.update_layout(
                            xaxis_title='time (days)', 
                            yaxis_title='Seed Moisture change per day (d.b. %/day)', 
                            xaxis_range=[0, time_day[-1]],
                            xaxis=dict(tick0=0, dtick=0.5),
                            # yaxis_range=[0, 1],
                            legend=dict(orientation='h', 
                                        yanchor='top', 
                                        y=1.12
                                        ))
        
        

        if (M_25 - Meq_doe) * 100 < mois_diff_doe:
            notice = dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Successful!")),
                            dbc.ModalBody("Good hole size is selected to match the threshold!"),
                        ],
                        size="lg",
                        is_open=True,
                    )
            str_compare = f"{round(M_25*100- Meq_doe*100, 2)} < {mois_diff_doe}"

        else:
            
            notice = dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Failed!")),
                            dbc.ModalBody("Hole size should be increased to accelerate drying."),
                        ],
                        size="lg",
                        is_open=True,
                    )
            str_compare = f"{round(M_25*100- Meq_doe*100, 2)} >= {mois_diff_doe}"

        report_table =  table(
                columnName=["Hole size [mm]", f"Seed moisture at {end_day_doe} days [d.b.%]", "Equilibrium seed moisture [d.b.%]", "Moisture gap [d.b.%]"],
                columnType=["numeric", "numeric", "numeric", "numeric"],
                tableID = "report_table",
                editable=False,
                row_deletable=False,
                row_selectable=False,
                # style_data = {'textAlign': 'center',},
                style_header= {'backgroundColor': 'rgb(192,192,192)','fontWeight': 'bold','font-size': '15px', 'textAlign': 'center'},
                data= [[hole_size_doe], [round(M_25*100, 2)], [round(Meq_doe*100,2)], [str_compare]]
            )

        return notice, report_table, [dcc.Graph(figure=pred_plot),dcc.Graph(figure=M_change_plot)]

"""