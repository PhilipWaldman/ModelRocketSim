import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Output, Input

import thrust_curve as tc
from app import app
from constants import g


def get_layout():
    return html.Div([
        html.H3('Plots'),
        dcc.Graph(id='altitude-time-graph')
    ],
        style={
            'margin-left': '2rem',
            'margin-right': '2rem'
        }
    )


@app.callback(
    Output('altitude-time-graph', 'figure'),
    Input('rocket-builder-data', 'data'),
    Input('thrust-curve-data', 'data'))
def altitude_time_graph(rocket_data, motor_data):
    # Load rocket and motor from Store
    mass = 1
    if rocket_data and '' in rocket_data.keys():
        mass = rocket_data['mass'] / 1000
    motor_file = tc.thrust_files[0]
    if motor_data and 'motor_file' in motor_data.keys():
        motor_file = motor_data['motor_file']
    motor_tc = tc.ThrustCurve(motor_file).thrust_curve

    xy = {}
    y = 0
    v = 0
    t0 = 0
    for t, F in motor_tc.items():
        a = F / mass
        v += a * (t - t0)
        y += v * (t - t0)
        xy[t] = y
        t0 = t
    dt = 0.01
    while y > 0:
        t0 += dt
        a = -g
        v += a * dt
        y += v * dt
        xy[t0] = y

    fig = px.line(x=xy.keys(), y=xy.values(), title='Altitude-time')
    fig.update_xaxes(range=[-0.025 * max(xy.keys()), 1.025 * max(xy.keys())])
    return fig
