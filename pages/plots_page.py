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
    m = 1
    if rocket_data and 'mass' in rocket_data.keys():
        m = rocket_data['mass'] / 1000
    motor_file = tc.thrust_files[0]
    if motor_data and 'motor_file' in motor_data.keys():
        motor_file = motor_data['motor_file']
    motor_tc = tc.ThrustCurve(motor_file).thrust_curve_smooth(dt)

    altitude = {}
    velocity = {}
    acceleration = {}
    y = 0
    v = 0
    for t, F in motor_tc.items():
        a = F / m - g
        v += a * dt
        y += v * dt
        if y < 0:
            y = 0
            v = 0
        altitude[t] = y
        velocity[t] = v
        acceleration[t] = a
    t = max(motor_tc.keys())
    while y > 0:
        t += dt
        a = - g
        v += a * dt
        y += v * dt
        altitude[t] = y
        velocity[t] = v
        acceleration[t] = a

    x_range = [-0.025 * max(altitude.keys()), 1.025 * max(altitude.keys())]

    fig_alt = px.line(x=altitude.keys(), y=altitude.values(), title='Altitude-time')
    fig_alt.update_xaxes(range=x_range)
    fig_alt.update_layout(xaxis_title_text='Time (s)',
                          yaxis_title_text='Altitude (m)')

    fig_vel = px.line(x=velocity.keys(), y=velocity.values(), title='Velocity-time')
    fig_vel.update_xaxes(range=x_range)
    fig_vel.update_layout(xaxis_title_text='Time (s)',
                          yaxis_title_text='Velocity (m/s)')

    fig_acc = px.line(x=acceleration.keys(), y=acceleration.values(), title='Acceleration-time')
    fig_acc.update_xaxes(range=x_range)
    fig_acc.update_layout(xaxis_title_text='Time (s)',
                          yaxis_title_text='Altitude (m/s^2)')

    return fig_alt, fig_vel, fig_acc
