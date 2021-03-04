import dash
import dash_daq as daq
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

from app import app
from conversions import metric_convert
from pages.rocket_builder import fins_page, nose_cone_page, body_tube_page

inputs = [
    {'name': 'mass', 'unit': 'g', 'default_value': 100, 'input_prefix': '-', 'si_prefix': 'k'},
    {'name': 'body tube length', 'unit': 'cm', 'default_value': 50, 'input_prefix': 'c', 'si_prefix': '-'},
    {'name': 'diameter', 'unit': 'cm', 'default_value': 5, 'input_prefix': 'c', 'si_prefix': '-'},
    {'name': 'nose cone length', 'unit': 'cm', 'default_value': 15, 'input_prefix': 'c', 'si_prefix': '-'},
    {'name': 'number of fins', 'unit': '', 'default_value': 4, 'input_prefix': '-', 'si_prefix': '-'},
    {'name': 'root chord', 'unit': 'cm', 'default_value': 5, 'input_prefix': 'c', 'si_prefix': '-'},
    {'name': 'tip chord', 'unit': 'cm', 'default_value': 5, 'input_prefix': 'c', 'si_prefix': '-'},
    {'name': 'fin height', 'unit': 'cm', 'default_value': 3, 'input_prefix': 'c', 'si_prefix': '-'},
    {'name': 'sweep length', 'unit': 'cm', 'default_value': 2.5, 'input_prefix': 'c', 'si_prefix': '-'}
]
pathname = '/rocket_builder'


@app.callback(
    Output('url', 'pathname'),
    Input('nose-cone-page-button', 'n_clicks'),
    Input('body-tube-page-button', 'n_clicks'),
    Input('fins-page-button', 'n_clicks')
)
def fin_page_button(nose_cone_clicks, body_tube_clicks, fins_clicks):
    if nose_cone_clicks is None and body_tube_clicks is None and fins_clicks is None:
        raise PreventUpdate
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'nose-cone-page-button' in changed_id:
        page = '/nose_cone'
    elif 'body-tube-page-button' in changed_id:
        page = '/body_tube'
    elif 'fins-page-button' in changed_id:
        page = '/fins'
    else:
        page = ''
    return f'{pathname}{page}'


def get_layout(data, url):
    if url.endswith('nose_cone'):
        return nose_cone_page.get_layout(data)
    elif url.endswith('body_tube'):
        return body_tube_page.get_layout(data)
    elif url.endswith('fins'):
        return fins_page.get_layout(data)

    layout = [
        html.H3('Rocket builder'),
        html.Div(html.Button('Nose cone', id='nose-cone-page-button')),
        html.Div(html.Button('Body tube', id='body-tube-page-button')),
        html.Div(html.Button('Fins', id='fins-page-button'))
    ]

    # # Load the current motor from Store
    # if data is None:
    #     data = {}
    # for i in inputs:
    #     if i['name'] not in data:
    #         data[i['name']] = metric_convert(i['default_value'], i['input_prefix'], i['si_prefix'])
    #
    # for i in inputs:
    #     name = i['name']
    #     unit = i['unit']
    #     value = i['default_value']
    #     if name in data.keys():
    #         value = metric_convert(data[name], i['si_prefix'], i['input_prefix'])
    #     layout.extend([
    #         html_name(name),
    #         html_numeric_input(name, value),
    #         html_unit(unit),
    #         html.Div()])
    #
    # layout.append(dcc.Graph(id='rocket-drawing'))

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
    Input('body-tube-length-input', 'value'),
    Input('diameter-input', 'value'),
    Input('nose-cone-length-input', 'value'),
    Input('root-chord-input', 'value'),
    Input('tip-chord-input', 'value'),
    Input('fin-height-input', 'value'),
    Input('sweep-length-input', 'value')
)
def draw_rocket(tube_length: float, diameter: float, nose_length: float, root_chord: float, tip_chord: float,
                fin_height: float, sweep_length: float):
    length = nose_length + tube_length
    radius = diameter / 2
    nose_cone = {'x': [0, nose_length, nose_length, 0],
                 'y': [0, radius, -radius, 0]}
    body = {'x': [nose_length, nose_length, length, length, nose_length],
            'y': [radius, -radius, -radius, radius, radius]}
    fin = {'x': [length, length - root_chord, length + sweep_length - tip_chord, length + sweep_length, length],
           'y': [radius, radius, radius + fin_height, radius + fin_height, radius]}

    x = []
    x.extend([i for i in nose_cone['x']])
    x.append(None)
    x.extend([i for i in body['x']])
    x.append(None)
    x.extend([i for i in fin['x']])
    x.append(None)
    x.extend([i for i in fin['x']])
    y = []
    y.extend([i for i in nose_cone['y']])
    y.append(None)
    y.extend([i for i in body['y']])
    y.append(None)
    y.extend([i for i in fin['y']])
    y.append(None)
    y.extend([-i for i in fin['y']])

    fig = go.Figure(
        go.Scatter(x=x,
                   y=y,
                   fill='toself'))
    fig.update_layout(plot_bgcolor='white')
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False, scaleanchor='x', scaleratio=1)

    return fig


@app.callback(
    Output('rocket-builder-data', 'data'),
    Input('mass-input', 'value'),
    Input('body-tube-length-input', 'value'),
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
