from os import listdir
from os.path import isfile, join

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import thrust_curves
from app import app

thrust_folder = 'thrustcurve'
thrust_files = [f for f in listdir(thrust_folder) if isfile(join(thrust_folder, f)) and f != '00INDEX.txt']

layout = html.Div([
    html.H3('Thrust curve'),
    dcc.Dropdown(
        id='thrust-curve-dropdown',
        options=[
            {'label': tc.split('.')[0].replace('_', ' ', 1).replace('_', '-', 1), 'value': tc} for tc in thrust_files
        ],
        value='AeroTech_G8'
    ),
    dcc.Graph(id='thrust-curve')
])


@app.callback(
    Output('thrust-curve', 'figure'),
    Input('thrust-curve-dropdown', 'value'))
def display_value(value):
    thrust_curve = thrust_curves.read_thrust_curve(value)
    return thrust_curves.get_thrust_curve_plot(thrust_curve, value)
