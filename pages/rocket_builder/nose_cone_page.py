import dash_html_components as html
from dash.dependencies import Output, Input

import pages.rocket_builder.rocket_builder_page as rb
from app import app
from conversions import metric_convert

inputs = {
    'nose cone length': {'unit': 'cm', 'default_value': 10, 'input_prefix': 'c', 'si_prefix': '-'}
}


def get_layout(data):
    layout = [html.H3('Nose cone')]
    layout.extend([rb.simple_input(i,
                                   metric_convert(data[i.replace(' ', '_')],
                                                  inputs[i]['si_prefix'],
                                                  inputs[i]['input_prefix']),
                                   inputs[i]['unit'])
                   for i in inputs])
    return layout


@app.callback(
    Output('nose-cone-builder-data', 'data'),
    Input('nose-cone-length-input', 'value')
)
def save_data(nose_cone_length: float):
    return {
        'nose_cone_length': round(
            metric_convert(nose_cone_length,
                           inputs['nose cone length']['input_prefix'],
                           inputs['nose cone length']['si_prefix']),
            4)
    }


def init_data(data):
    if 'nose_cone_length' not in data.keys():
        data['nose_cone_length'] = rb.convert_default_input('nose cone length', inputs)
