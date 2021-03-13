import dash_html_components as html
from dash.dependencies import Output, Input

import pages.rocket_builder.rocket_builder_page as rb
from app import app
from conversions import metric_convert

inputs = {
    'diameter': {'unit': 'cm', 'default_value': 30, 'input_prefix': 'c', 'si_prefix': '-'},
    'drag coefficient': {'unit': '', 'default_value': 0.8, 'input_prefix': '-', 'si_prefix': '-'},
    'deploy delay': {'unit': 's', 'default_value': 3, 'input_prefix': '-', 'si_prefix': '-'}
}


def get_layout(data):
    layout = [html.H3('Recovery')]
    layout.extend([rb.simple_input(i,
                                   metric_convert(data[f'parachute_{i.replace(" ", "_")}'],
                                                  inputs[i]['si_prefix'],
                                                  inputs[i]['input_prefix']),
                                   inputs[i]['unit'],
                                   id=f'chute-{i.replace(" ", "-")}-input')
                   for i in inputs])
    return layout


@app.callback(
    Output('recovery-builder-data', 'data'),
    Input('chute-deploy-delay-input', 'value'),
    Input('chute-drag-coefficient-input', 'value'),
    Input('chute-diameter-input', 'value')
)
def save_data(deploy_delay: float, drag_coefficient: float, diameter: float):
    return {
        'parachute_deploy_delay': round(deploy_delay, 4),
        'parachute_drag_coefficient': round(drag_coefficient, 4),
        'parachute_diameter': round(
            metric_convert(diameter,
                           inputs['diameter']['input_prefix'],
                           inputs['diameter']['si_prefix']),
            4)
    }


def init_data(data):
    if 'parachute_diameter' not in data.keys():
        data['parachute_diameter'] = rb.convert_default_input('diameter', inputs)
    if 'parachute_drag_coefficient' not in data.keys():
        data['parachute_drag_coefficient'] = rb.convert_default_input('drag coefficient', inputs)
    if 'parachute_deploy_delay' not in data.keys():
        data['parachute_deploy_delay'] = rb.convert_default_input('deploy delay', inputs)
