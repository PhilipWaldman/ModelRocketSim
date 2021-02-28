import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Output, Input

from app import app


def get_layout(data):
    # Load the current motor from Store
    if not data:
        data = {}

    layout = [html.H3('Rocket builder')]

    inputs = [
        {'name': 'mass', 'unit': 'g', 'conversion_factor': 1000, 'default_value': 100},
        {'name': 'length', 'unit': 'cm', 'conversion_factor': 100, 'default_value': 50},
        {'name': 'diameter', 'unit': 'cm', 'conversion_factor': 100, 'default_value': 5}
    ]

    for i in inputs:
        name = i['name']
        unit = i['unit']
        value = i['default_value']
        if name in data.keys():
            value = data[name] * i['conversion_factor']
        layout.extend([
            html_name(name),
            html_numeric_input(name, value),
            html_unit(unit),
            html.Div()])

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
    Output('rocket-builder-data', 'data'),
    Input('mass-input', 'value'),
    Input('length-input', 'value'),
    Input('diameter-input', 'value'))
def save_data(mass: float, length: float, diameter: float):
    """
    :param diameter: The diameter in centimeters (cm).
    :param length: The length in centimeters (cm).
    :param mass: The mass in grams (g).
    """
    return {'mass': mass / 1000,
            'length': length / 100,
            'diameter': diameter / 100}
