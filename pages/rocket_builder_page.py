import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Output, Input

from app import app
from conversions import metric_convert

inputs = [
    {'name': 'mass', 'unit': 'g', 'default_value': 100, 'input_prefix': '-', 'si_prefix': 'k'},
    {'name': 'length', 'unit': 'cm', 'default_value': 50, 'input_prefix': 'c', 'si_prefix': '-'},
    {'name': 'diameter', 'unit': 'cm', 'default_value': 5, 'input_prefix': 'c', 'si_prefix': '-'}
]


def get_layout(data):
    # Load the current motor from Store
    if data is None:
        data = {}
    for i in inputs:
        if i['name'] not in data:
            data[i['name']] = metric_convert(i['default_value'], i['input_prefix'], i['si_prefix'])

    layout = [html.H3('Rocket builder')]

    for i in inputs:
        name = i['name']
        unit = i['unit']
        value = i['default_value']
        if name in data.keys():
            value = metric_convert(data[name], i['si_prefix'], i['input_prefix'])
        layout.extend([
            html_name(name),
            html_numeric_input(name, value),
            html_unit(unit),
            html.Div()])

    layout.append(dcc.Graph(id='rocket-drawing'))

    return html.Div(layout,
                    style={'margin-left': '2rem',
                           'margin-right': '2rem'})


def html_name(name: str):
    """ :param name: The name of the input. Should be lowercase with spaces between words. """
    return html.P(f'{name.capitalize()}:',
                  style={'width': '10%',
                         'display': 'inline-block',
                         'margin-right': '1rem'})


def html_numeric_input(name: str, value: float):
    """
    :param name: The name of the input. Should be lowercase with spaces between words.
    :param value: The default value of the input.
    """
    return html.Div(
        daq.NumericInput(
            id=f'{name.replace(" ", "-")}-input',
            size=64,
            min=0,
            max=10 ** 9,
            value=value),
        style={'display': 'inline-block',
               'margin-right': '1rem'})


def html_unit(unit: str):
    """ :param unit: The unit of the input. """
    return html.P(unit,
                  style={'width': '1%',
                         'display': 'inline-block'})


@app.callback(
    Output('rocket-drawing', 'figure'),
    Input('length-input', 'value'),
    Input('diameter-input', 'value'))
def draw_rocket(length: float, diameter: float):
    nose_cone = {'x': [0, 0.2, 0.2, 0], 'y': [0, 0.5, -0.5, 0]}
    body = {'x': [0.2, 0.2, 1, 1, 0.2], 'y': [0.5, -0.5, -0.5, 0.5, 0.5]}
    fin = {'x': [0.8, 1, 1, 0.8], 'y': [0.5, 0.5, 1, 0.5]}

    x = []
    x.extend([i * length for i in nose_cone['x']])
    x.append(None)
    x.extend([i * length for i in body['x']])
    x.append(None)
    x.extend([i * length for i in fin['x']])
    x.append(None)
    x.extend([i * length for i in fin['x']])
    y = []
    y.extend([i * diameter for i in nose_cone['y']])
    y.append(None)
    y.extend([i * diameter for i in body['y']])
    y.append(None)
    y.extend([i * diameter for i in fin['y']])
    y.append(None)
    y.extend([-i * diameter for i in fin['y']])

    fig = go.Figure(
        go.Scatter(x=x,
                   y=y,
                   fill='toself'))
    fig.update_layout(plot_bgcolor='white')
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False, scaleanchor="x", scaleratio=1)

    return fig


@app.callback(
    Output('rocket-builder-data', 'data'),
    Input('mass-input', 'value'),
    Input('length-input', 'value'),
    Input('diameter-input', 'value'))
def save_data(mass: float, length: float, diameter: float):
    """

    :param mass: The mass in grams (g).
    :param length: The length in centimeters (cm).
    :param diameter: The diameter in centimeters (cm).
    """
    return {'mass': metric_convert(mass, '-', 'k'),
            'length': metric_convert(length, 'c', '-'),
            'diameter': metric_convert(diameter, 'c', '-')}
