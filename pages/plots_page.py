import math

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Output, Input

import thrust_curve as tc
from app import app
from constants import g

pathname = '/plots'
page_name = 'Plots'


def get_layout():
    return html.Div([
        html.H3(page_name),
        dcc.Loading(
            id='loading-altitude-time-graph',
            type='dot',
            children=dcc.Graph(id='altitude-time-graph')
        ),
        dcc.Loading(
            id='loading-velocity-time-graph',
            type='dot',
            children=dcc.Graph(id='velocity-time-graph')
        ),
        dcc.Loading(
            id='loading-acceleration-time-graph',
            type='dot',
            children=dcc.Graph(id='acceleration-time-graph')
        )
    ],
        style={
            'margin-left': '2rem',
            'margin-right': '2rem'
        }
    )


@app.callback(
    Output('altitude-time-graph', 'figure'),
    Output('velocity-time-graph', 'figure'),
    Output('acceleration-time-graph', 'figure'),
    Input('rocket-builder-data', 'data'),
    Input('thrust-curve-data', 'data'))
def altitude_time_graph(rocket_data, motor_data):
    dt = 0.01
    # Load rocket and motor from Store
    m = 0.1
    l = 0.5
    d = 0.05
    if rocket_data:
        if 'mass' in rocket_data.keys():
            m = rocket_data['mass']
        if 'length' in rocket_data.keys():
            l = rocket_data['length']
        if 'diameter' in rocket_data.keys():
            d = rocket_data['diameter']
    motor_file = tc.thrust_files[0]
    if motor_data and 'motor_file' in motor_data.keys():
        motor_file = motor_data['motor_file']
    motor_tc = tc.ThrustCurve(motor_file).thrust_curve

    altitude = {}
    velocity = {}
    acceleration = {}
    y = 0
    v = 0
    t = 0
    for t1, F_thrust in motor_tc.items():
        F = F_thrust - g * m - calc_drag_force(v, d)
        a = F / m
        v += a * (t1 - t)
        y += v * (t1 - t)
        if y < 0:
            y = 0
            v = 0
        altitude[t1] = y
        velocity[t1] = v
        acceleration[t1] = a
        t = t1
    dt = 0.01
    while y > 0:
        t += dt
        F = - g * m - calc_drag_force(v, d)
        a = F / m
        v += a * dt
        y += v * dt
        altitude[t] = y
        velocity[t] = v
        acceleration[t] = a

    x_range = [-0.025 * max(altitude.keys()), 1.025 * max(altitude.keys())]

    # ------------------------------ Altitude ------------------------------
    fig_alt = go.Figure(go.Scatter(x=list(altitude.keys()),
                                   y=list(altitude.values()),
                                   mode='lines',
                                   hovertemplate='<b>%{text}</b>',
                                   text=[f't = {round(time, 3)} s<br>'
                                         f'y = {round(alt, 3)} m'
                                         for time, alt in altitude.items()]))
    fig_alt.update_layout(title_text='Altitude-time',
                          xaxis_title_text='Time (s)',
                          yaxis_title_text='Altitude (m)')
    fig_alt.update_xaxes(range=x_range)

    # ------------------------------ Velocity ------------------------------
    fig_vel = go.Figure(go.Scatter(x=list(velocity.keys()),
                                   y=list(velocity.values()),
                                   mode='lines',
                                   hovertemplate='<b>%{text}</b>',
                                   text=[f't = {round(time, 3)} s<br>'
                                         f'v = {round(vel, 3)} m/s'
                                         for time, vel in velocity.items()]))
    fig_vel.update_layout(title_text='Velocity-time',
                          xaxis_title_text='Time (s)',
                          yaxis_title_text='Velocity (m/s)')
    fig_vel.update_xaxes(range=x_range)

    # ------------------------------ Acceleration ------------------------------
    fig_acc = go.Figure(go.Scatter(x=list(acceleration.keys()),
                                   y=list(acceleration.values()),
                                   mode='lines',
                                   hovertemplate='<b>%{text}</b>',
                                   text=[f't = {round(time, 3)} s<br>'
                                         f'a = {round(acc, 3)} m/s^2'
                                         for time, acc in acceleration.items()]))
    fig_acc.update_layout(title_text='Acceleration-time',
                          xaxis_title_text='Time (s)',
                          yaxis_title_text='Acceleration (m/s)')
    fig_acc.update_xaxes(range=x_range)

    return fig_alt, fig_vel, fig_acc


def calc_drag_force(v, d):
    """ F_drag = 0.5 * Cd * ρ * v^2 * A

    https://www.grc.nasa.gov/www/k-12/airplane/drageq.html

    :param v: Velocity
    :param d: Diameter
    :return: The drag force
    """
    return 0.5 * 0.37 * 1.205 * (v ** 2) * ((d / 2) ** 2 * math.pi)
