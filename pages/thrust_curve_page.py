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
manufacturer_options = [{'label': m, 'value': m} for m in manufacturers]
manufacturer_options.append({'label': '<all>', 'value': '<all>'})


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
        # TODO: add filters to narrow down motor options
        # Select by:
        # 'manufacturer'
        dcc.Dropdown(
            id='manufacturer-dropdown',
            options=manufacturer_options,
            value='<all>'),
        # 'diameter'
        # 'length'
        # 'impulse'
        # 'avg_thrust'
        # 'burn_time'
        # 'impulse_range' - Not implemented yet
        dcc.Graph(id='thrust-curve'),
    ],
        style={
            'margin-left': '2rem',
            'margin-right': '2rem'
        }
    )


@app.callback(
    Output('thrust-curve-dropdown', 'options'),
    Input('manufacturer-dropdown', 'value')
)
def filter_manufacturer(manufacturer: str):
    if manufacturer == '<all>':
        return motor_options
    return [{'label': str(tc), 'value': tc.file_name}
            for tc in thrust_curves
            if tc.manufacturer == manufacturer]


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
