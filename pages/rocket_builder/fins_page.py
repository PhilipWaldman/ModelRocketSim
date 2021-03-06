import dash_html_components as html
from dash.dependencies import Output, Input

import pages.rocket_builder.rocket_builder_page as rb
from app import app
from conversions import metric_convert

inputs = {
    'number of fins': {'unit': '', 'default_value': 3, 'input_prefix': '-', 'si_prefix': '-'},
    'root chord': {'unit': 'cm', 'default_value': 5, 'input_prefix': 'c', 'si_prefix': '-'},
    'tip chord': {'unit': 'cm', 'default_value': 5, 'input_prefix': 'c', 'si_prefix': '-'},
    'fin height': {'unit': 'cm', 'default_value': 3, 'input_prefix': 'c', 'si_prefix': '-'},
    'sweep length': {'unit': 'cm', 'default_value': 2.5, 'input_prefix': 'c', 'si_prefix': '-'}
}


def get_layout(data):
    layout = [html.H3('Fins')]
    layout.extend([rb.simple_input(i,
                                   metric_convert(data[i.replace(' ', '_')],
                                                  inputs[i]['si_prefix'],
                                                  inputs[i]['input_prefix']),
                                   inputs[i]['unit'])
                   for i in inputs])
    return layout


@app.callback(
    Output('fin-builder-data', 'data'),
    Input('number-of-fins-input', 'value'),
    Input('root-chord-input', 'value'),
    Input('tip-chord-input', 'value'),
    Input('fin-height-input', 'value'),
    Input('sweep-length-input', 'value')
)
def save_data(number_of_fins: int, root_chord: float, tip_chord: float, fin_height: float, sweep_length: float):
    return {
        'number_of_fins': metric_convert(number_of_fins,
                                         inputs['number of fins']['input_prefix'],
                                         inputs['number of fins']['si_prefix']),
        'root_chord': metric_convert(root_chord,
                                     inputs['root chord']['input_prefix'],
                                     inputs['root chord']['si_prefix']),
        'tip_chord': metric_convert(tip_chord,
                                    inputs['tip chord']['input_prefix'],
                                    inputs['tip chord']['si_prefix']),
        'fin_height': metric_convert(fin_height,
                                     inputs['fin height']['input_prefix'],
                                     inputs['fin height']['si_prefix']),
        'sweep_length': metric_convert(sweep_length,
                                       inputs['sweep length']['input_prefix'],
                                       inputs['sweep length']['si_prefix'])
    }


def init_data(data):
    if 'number_of_fins' not in data.keys():
        data['number_of_fins'] = rb.convert_default_input('number of fins', inputs)
    if 'root_chord' not in data.keys():
        data['root_chord'] = rb.convert_default_input('root chord', inputs)
    if 'sweep_length' not in data.keys():
        data['sweep_length'] = rb.convert_default_input('sweep length', inputs)
    if 'tip_chord' not in data.keys():
        data['tip_chord'] = rb.convert_default_input('tip chord', inputs)
    if 'fin_height' not in data.keys():
        data['fin_height'] = rb.convert_default_input('fin height', inputs)
