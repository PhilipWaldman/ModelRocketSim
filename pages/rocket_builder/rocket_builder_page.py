import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from app import app
from conversions import metric_convert
from pages import page404
from pages.rocket_builder import fins_page, nose_cone_page, body_tube_page

pathname = '/rocket_builder'
page_name = 'Rocket builder'
cur_page = ''  # main, fins, body tube, nose cone


@app.callback(
    Output('url', 'pathname'),
    Input('nose-cone-page-button', 'n_clicks'),
    Input('body-tube-page-button', 'n_clicks'),
    Input('fins-page-button', 'n_clicks')
)
def change_page(nose_cone_clicks, body_tube_clicks, fins_clicks):
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
    if data is None:
        data = {}
        init_data(data)

    global cur_page
    if url.endswith('nose_cone'):
        cur_page = 'nose cone'
        layout = nose_cone_page.get_layout(data)
    elif url.endswith('body_tube'):
        cur_page = 'body tube'
        layout = body_tube_page.get_layout(data)
    elif url.endswith('fins'):
        cur_page = 'fins'
        layout = fins_page.get_layout(data)
    elif url.endswith(pathname):
        cur_page = 'main'
        layout = [
            html.H3('Rocket builder'),
            html.Div(html.Button('Nose cone', id='nose-cone-page-button')),
            html.Div(html.Button('Body tube', id='body-tube-page-button')),
            html.Div(html.Button('Fins', id='fins-page-button'))
        ]
    else:
        cur_page = ''
        return page404.layout

    layout.append(dcc.Graph(id='rocket-drawing'))

    layout.extend([
        dcc.Store(id='fin-builder-data'),
        dcc.Store(id='body-tube-builder-data'),
        dcc.Store(id='nose-cone-builder-data')
    ])

    return html.Div(layout,
                    style={'margin-left': '2rem',
                           'margin-right': '2rem'})


def simple_input(name: str, value: float, unit: str):
    """ Constructs a simple numeric input. It displays the name of the input, a numeric input field with an initial
    value, and a unit behind it.

    :param name: The name of the input. Should be lowercase with spaces between words.
    :param value: The default value of the input.
    :param unit: The unit of the input.
    :return: A simple input.
    """
    return html.Div([
        html_name(name),
        html_numeric_input(name, value),
        html_unit(unit)
    ])


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
            size=100,
            min=0,
            max=10 ** 9,
            value=round(value, 3)),
        style={'display': 'inline-block',
               'margin-right': '1rem'})


def html_unit(unit: str):
    """ :param unit: The unit of the input. """
    return html.P(unit,
                  style={'width': '1%',
                         'display': 'inline-block'})


@app.callback(
    Output('rocket-drawing', 'figure'),
    Input('rocket-builder-data', 'modified_timestamp'),
    State('rocket-builder-data', 'data')
)
def draw_rocket(ts, data):
    if ts is None or data is None:
        raise PreventUpdate

    nose_length = data['nose_cone_length']
    tube_length = data['body_tube_length']
    diameter = data['diameter']
    root_chord = data['root_chord']
    sweep_length = data['sweep_length']
    tip_chord = data['tip_chord']
    fin_height = data['fin_height']

    length = nose_length + tube_length
    radius = diameter / 2
    nose_cone = {'x': [0, nose_length, nose_length, 0],
                 'y': [0, radius, -radius, 0]}
    body = {'x': [nose_length, nose_length, length, length, nose_length],
            'y': [radius, -radius, -radius, radius, radius]}
    fin = {'x': [length, length - root_chord, length - root_chord + sweep_length,
                 length - root_chord + sweep_length + tip_chord, length],
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
    Input('nose-cone-builder-data', 'data'),
    Input('body-tube-builder-data', 'data'),
    Input('fin-builder-data', 'data'),
    State('rocket-builder-data', 'data')
)
def save_data(nose_cone, body_tube, fins, data):
    data = data or {}
    init_data(data)
    if nose_cone is not None:
        for key, val in nose_cone.items():
            data[key] = val
    if body_tube is not None:
        for key, val in body_tube.items():
            data[key] = val
    if fins is not None:
        for key, val in fins.items():
            data[key] = val
    return data


def init_data(data):
    nose_cone_page.init_data(data)
    body_tube_page.init_data(data)
    fins_page.init_data(data)


def convert_default_input(name: str, inputs: dict[str, dict]) -> float:
    return metric_convert(inputs[name]['default_value'],
                          inputs[name]['input_prefix'],
                          inputs[name]['si_prefix'])
