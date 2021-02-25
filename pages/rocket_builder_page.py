import json
from os import path

import dash_html_components as html

# The path to save the data file.
save_path = path.join('data', 'rocket_builder_data.json')


def get_layout():
    # TODO: Load rocket config from the data file

    return html.Div([
        html.H3('Rocket builder'),

    ],
        style={
            'margin-left': '2rem',
            'margin-right': '2rem'
        }
    )


def save_data():
    data_dict = {}
    with open(save_path, 'w') as outfile:
        json.dump(data_dict, outfile)
