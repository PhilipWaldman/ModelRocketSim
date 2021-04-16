from math import ceil, floor

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from app import app
from thrust_curve import thrust_curves, ThrustCurve

pathname = '/thrust_curves'
page_name = 'Thrust curves'

# The option for the dropdown. List of pairs of motor names and file names.
motor_options = [{'label': str(tc), 'value': tc.file_name} for tc in thrust_curves]
# The manufacturers to show in the selector dropdown.
manufacturers = sorted(set([tc.manufacturer for tc in thrust_curves]))
manufacturer_options = [{'label': '<all>', 'value': '<all>'}]
manufacturer_options.extend([{'label': m, 'value': m} for m in manufacturers])
# All unique diameters
diameters = sorted({tc.diameter for tc in thrust_curves})
# Min and max length
lengths = {tc.length for tc in thrust_curves}
lengths = [min(lengths), max(lengths)]
# Min and max impulse
impulses = {tc.impulse for tc in thrust_curves}
impulses = [min(impulses), max(impulses)]
# Min and max avg_thrust
avg_thrusts = {tc.avg_thrust for tc in thrust_curves}
avg_thrusts = [min(avg_thrusts), max(avg_thrusts)]
# Min and max burn_time
burn_times = {tc.burn_time for tc in thrust_curves}
burn_times = [min(burn_times), max(burn_times)]


def get_layout(data):
    # Load the current motor from Store
    if data:
        cur_motor = data['motor_file']
    else:
        cur_motor = thrust_curves[0].file_name

    return html.Div([
        html.H3(page_name),
        dcc.Dropdown(
            id='thrust-curve-dropdown',
            options=motor_options,
            value=cur_motor),
        # Filter by:
        # manufacturer
        html.Div([
            html.P('Manufacturer: ',
                   style={'display': 'inline-block', 'width': '10%'}),
            html.Div(
                dcc.Dropdown(
                    id='manufacturer-dropdown',
                    options=manufacturer_options,
                    value='<all>'),
                style={'display': 'inline-block', 'width': '90%'}
            )
        ]),
        # diameter
        html.Div([
            html.P('Diameter: ',
                   style={'display': 'inline-block', 'width': '10%'}),
            html.Div(
                dcc.RangeSlider(
                    id='diameter-slider',
                    min=0,
                    max=len(diameters) - 1,
                    step=None,
                    marks=dict([(i, str(d)) for i, d in enumerate(diameters)]),
                    value=[0, len(diameters) - 1]),
                style={'display': 'inline-block', 'width': '90%'})
        ]),
        # length
        continuous_range_slider('length', lengths),
        # impulse
        continuous_range_slider('impulse', impulses),
        # avg_thrust
        continuous_range_slider('thrust', avg_thrusts),
        # burn_time
        continuous_range_slider('burn time', burn_times, 1),
        # impulse_range - Not implemented yet
        # continuous_range_slider('burn time', burn_times),
        dcc.Graph(id='thrust-curve'),
    ],
        style={
            'margin-left': '2rem',
            'margin-right': '2rem'
        }
    )


def continuous_range_slider(name: str, range_list: list, mark_step_size: int = None):
    if not mark_step_size:
        mark_step_size = int((range_list[-1] - range_list[0]) / 20)
    return html.Div([
        html.P(f'{name.capitalize()}: ',
               style={'display': 'inline-block', 'width': '10%'}),
        html.P(range_list[0],
               id=f'min-{name}-text'.replace(' ', '-'),
               style={'display': 'inline-block', 'width': '1%'}),
        html.Div(
            dcc.RangeSlider(
                id=f'{name}-slider'.replace(' ', '-'),
                min=floor(range_list[0]),
                max=ceil(range_list[-1]),
                marks=dict([(i, str(i))
                            for i in range(floor(range_list[0]),
                                           ceil(range_list[-1] + 1),
                                           mark_step_size)
                            ]),
                value=[floor(range_list[0]), ceil(range_list[-1])]),
            style={'display': 'inline-block', 'width': '84%'}),
        html.P(range_list[-1],
               id=f'max-{name}-text'.replace(' ', '-'),
               style={'display': 'inline-block', 'width': '5%'}),
    ])


@app.callback(
    Output('thrust-curve-dropdown', 'options'),
    Output('min-length-text', 'children'),
    Output('max-length-text', 'children'),
    Output('min-impulse-text', 'children'),
    Output('max-impulse-text', 'children'),
    Output('min-thrust-text', 'children'),
    Output('max-thrust-text', 'children'),
    Output('min-burn-time-text', 'children'),
    Output('max-burn-time-text', 'children'),
    Input('manufacturer-dropdown', 'value'),
    Input('diameter-slider', 'value'),
    Input('length-slider', 'value'),
    Input('impulse-slider', 'value'),
    Input('thrust-slider', 'value'),
    Input('burn-time-slider', 'value')
)
def apply_filters(manufacturer: str, diameter_vals: list, length_vals: list, impulse_vals: list, thrust_vals: list,
                  burn_time_vals: list):
    curves = [tc for tc in thrust_curves if manufacturer == '<all>' or tc.manufacturer == manufacturer]
    curves = [tc for tc in curves if diameters[diameter_vals[0]] <= tc.diameter <= diameters[diameter_vals[-1]]]
    curves = [tc for tc in curves if length_vals[0] <= tc.length <= length_vals[-1]]
    curves = [tc for tc in curves if impulse_vals[0] <= tc.impulse <= impulse_vals[-1]]
    curves = [tc for tc in curves if thrust_vals[0] <= tc.avg_thrust <= thrust_vals[-1]]
    curves = [tc for tc in curves if burn_time_vals[0] <= tc.burn_time <= burn_time_vals[-1]]
    return [{'label': str(tc), 'value': tc.file_name} for tc in curves], \
           length_vals[0], length_vals[-1], \
           impulse_vals[0], impulse_vals[-1], \
           thrust_vals[0], thrust_vals[-1], \
           burn_time_vals[0], burn_time_vals[-1]


@app.callback(
    Output('thrust-curve', 'figure'),
    Output('thrust-curve-data', 'data'),
    Input('thrust-curve-dropdown', 'value')
)
def plot_thrust_curve(file_name: str):
    if file_name is None:
        return go.Figure()
    thrust_curve = ThrustCurve(file_name)
    return (thrust_curve.plot(),
            save_data(file_name))


def save_data(file_name: str):
    current_motor = ''
    for m in motor_options:
        if m['value'] == file_name:
            current_motor = m['label']
    data = {'motor_name': current_motor, 'motor_file': file_name}
    return data
