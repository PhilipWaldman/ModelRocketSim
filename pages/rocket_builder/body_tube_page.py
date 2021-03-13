import dash_html_components as html
from dash.dependencies import Output, Input

import pages.rocket_builder.rocket_builder_page as rb
from app import app
from conversions import metric_convert

inputs = {
    # TODO: mass is total mass for now. change so every component has separate mass that is added up.
    'mass': {'unit': 'g', 'default_value': 95, 'input_prefix': '-', 'si_prefix': 'k'},
    'body tube length': {'unit': 'cm', 'default_value': 45, 'input_prefix': 'c', 'si_prefix': '-'},
    'diameter': {'unit': 'cm', 'default_value': 3.5, 'input_prefix': 'c', 'si_prefix': '-'}
}


def get_layout(data):
    layout = [html.H3('Body tube')]
    layout.extend([rb.simple_input(i,
                                   metric_convert(data[i.replace(' ', '_')],
                                                  inputs[i]['si_prefix'],
                                                  inputs[i]['input_prefix']),
                                   inputs[i]['unit'])
                   for i in inputs])
    return layout


@app.callback(
    Output('body-tube-builder-data', 'data'),
    Input('mass-input', 'value'),
    Input('body-tube-length-input', 'value'),
    Input('diameter-input', 'value')
)
def save_data(mass: float, body_tube_length: float, diameter: float):
    return {
        # TODO: same as above about mass.
        'mass': round(
            metric_convert(mass,
                           inputs['mass']['input_prefix'],
                           inputs['mass']['si_prefix']),
            4),
        'body_tube_length': round(
            metric_convert(body_tube_length,
                           inputs['body tube length']['input_prefix'],
                           inputs['body tube length']['si_prefix']),
            4),
        'diameter': round(
            metric_convert(diameter,
                           inputs['diameter']['input_prefix'],
                           inputs['diameter']['si_prefix']),
            4)
    }


def init_data(data):
    # TODO: same as above about mass.
    if 'mass' not in data.keys():
        data['mass'] = rb.convert_default_input('mass', inputs)
    if 'body_tube_length' not in data.keys():
        data['body_tube_length'] = rb.convert_default_input('body tube length', inputs)
    if 'diameter' not in data.keys():
        data['diameter'] = rb.convert_default_input('diameter', inputs)
