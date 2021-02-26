import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Output, Input

from app import app


def get_layout(data):
    # Load the current motor from Store
    if not data:
        data = {}

    layout = [html.H3('Rocket builder')]
    options = {
        'mass': 'g'
        # 'length': 'cm',
        # 'diameter': 'cm',
        # 'center_of_gravity': 'cm',
        # 'center_of_pressure': 'cm'
    }

    for name, unit in options.items():
        value = 0
        if name in data.keys():
            value = data[name]

        layout.extend([
            html.P(f'{name.capitalize().replace("_", " ")}:',
                   style={'width': '10%',
                          'display': 'inline-block',
                          'margin-right': '1rem'}),
            html.Div(
                daq.NumericInput(
                    id=f'{name.replace("_", "-")}-input',
                    min=0,
                    value=value),
                style={'display': 'inline-block',
                       'margin-right': '1rem'}),
            html.P(unit,
                   style={'width': '1%',
                          'display': 'inline-block'}),
            html.Div()])

    return html.Div(layout,
                    style={'margin-left': '2rem',
                           'margin-right': '2rem'})


@app.callback(
    Output('rocket-builder-data', 'data'),
    Input('mass-input', 'value')
)
def save_data(mass):
    return {'mass': mass}
