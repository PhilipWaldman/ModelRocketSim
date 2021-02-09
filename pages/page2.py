import json
from os import path

import dash_html_components as html

from pages import thrust_curve_page


def read_cur_motor():
    p = thrust_curve_page.save_path
    if not path.exists(p):
        return ''
    with open(p, 'r') as file:
        data = json.load(file)
        return data['motor_name']


def get_layout():
    return html.Div([
        html.H3('Page 2'),
        html.P(f'Current motor: {read_cur_motor()}')
    ])
