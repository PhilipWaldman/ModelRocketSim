import json
from os import path

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import thrust_curve as tc
from app import app

# The option for the dropdown. List of pairs of motor names and file names.
motor_options = [{'label': m, 'value': f} for m, f in zip(tc.motor_names, tc.thrust_files)]
# The path to save the data file.
save_path = path.join('data', 'thrust_curve_page_data.json')


def get_layout():
    # Load the current motor from the data file
    cur_motor = tc.thrust_files[0]
    if path.exists(save_path):
        with open(save_path, 'r') as file:
            data = json.load(file)
            cur_motor = data['motor_file']

    return html.Div([
        html.H3('Thrust curve'),
        dcc.Dropdown(
            id='thrust-curve-dropdown',
            options=motor_options,
            value=cur_motor),
        # TODO: Add sliders to set ranges
        # dcc.RangeSlider(
        #     id='thrust-slider',
        #     min=0,
        #     max=20,
        #     step=0.5,
        #     value=[5, 15]
        # )
        dcc.Graph(id='thrust-curve')
    ],
        style={
            'margin-left': '2rem',
            'margin-right': '2rem'
        }
    )


@app.callback(
    Output('thrust-curve', 'figure'),
    Input('thrust-curve-dropdown', 'value'))
def plot_thrust_curve(file_name):
    save_data(file_name)
    if file_name is None:
        return go.Figure()
    thrust_curve = tc.ThrustCurve(file_name)
    return thrust_curve.get_thrust_curve_plot()


def save_data(file_name):
    current_motor = ''
    for m in motor_options:
        if m['value'] == file_name:
            current_motor = m['label']
    data_dict = {'motor_name': current_motor, 'motor_file': file_name}
    with open(save_path, 'w') as outfile:
        json.dump(data_dict, outfile)
