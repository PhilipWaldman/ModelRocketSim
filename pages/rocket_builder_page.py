import dash_daq as daq

import dash_html_components as html


def get_layout():
    layout = [html.H3('Rocket builder')]
    options = {
        'Mass': 'g',
        'Length': 'cm',
        'Diameter': 'cm',
        'Center of gravity': 'cm',
        'Center of pressure': 'cm'
    }

    for name, unit in options.items():
        layout.extend([
            html.P(f'{name}:',
                   style={'width': '10%',
                          'display': 'inline-block',
                          'margin-right': '1rem'}),
            html.Div(
                daq.NumericInput(
                    id=f'{name.lower().replace(" ", "-")}-input',
                    min=0,
                    value=0),
                style={'display': 'inline-block',
                       'margin-right': '1rem'}),
            html.P(unit,
                   style={'width': '1%',
                          'display': 'inline-block'}),
            html.Div()])

    return html.Div(layout,
                    style={'margin-left': '2rem',
                           'margin-right': '2rem'})
