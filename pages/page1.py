import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import thrust_curve as tc
from app import app

# TODO: add range sliders to narrow down thrust curves
layout = html.Div([
    html.H3('Thrust curve'),
    dcc.Dropdown(
        id='thrust-curve-dropdown',
        options=[
            {'label': m, 'value': f} for m, f in zip(tc.motor_names, tc.thrust_files)
        ],
        value=tc.thrust_files[0]
    ),
    dcc.Graph(id='thrust-curve')
])


@app.callback(
    Output('thrust-curve', 'figure'),
    Input('thrust-curve-dropdown', 'value'))
def display_value(file_name):
    thrust_curve = tc.ThrustCurve(file_name)
    return thrust_curve.get_thrust_curve_plot()
