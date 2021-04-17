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
def graphs(rocket_data, motor_data):
    dt = 0.01
    # Load rocket and motor from Store
    m = 0.1
    d = 0.05
    chute_d = 50
    chute_delay = 5
    chute_Cd = 1
    if rocket_data:
        if 'mass' in rocket_data.keys():
            m = rocket_data['mass']
        if 'diameter' in rocket_data.keys():
            d = rocket_data['diameter']
        if 'parachute_diameter' in rocket_data.keys():
            chute_d = rocket_data['parachute_diameter']
        if 'parachute_deploy_delay' in rocket_data.keys():
            chute_delay = rocket_data['parachute_deploy_delay']
        if 'parachute_drag_coefficient' in rocket_data.keys():
            chute_Cd = rocket_data['parachute_drag_coefficient']
    motor = tc.thrust_curves[0]
    if motor_data and 'motor_file' in motor_data.keys():
        motor = tc.ThrustCurve(motor_data['motor_file'])
    motor_tc = motor.thrust_curve

    altitude = {}
    velocity = {}
    acceleration = {}
    y = 0
    v = 0
    t = 0
    for t1, F_thrust in motor_tc.items():
        _, a, v, y = move(0, (t1 - t), F_thrust, v, y, m, d)
        altitude[t1] = y
        velocity[t1] = v
        acceleration[t1] = a
        t = t1
    burnout = t
    while y > 0:
        if t - burnout < chute_delay:
            t, a, v, y = move(t, dt, 0, v, y, m, d)
        else:
            t, a, v, y = move(t, dt, 0, v, y, m, chute_d, chute_Cd)
        altitude[t] = y
        velocity[t] = v
        acceleration[t] = a

    apogee = max(altitude.values())
    t_apogee = list(altitude.keys())[list(altitude.values()).index(apogee)]

    x_range = [-0.025 * max(altitude.keys()), 1.025 * max(altitude.keys())]

    # ------------------------------ Altitude ------------------------------
    alt_range = [min(altitude.values()) - 0.05 * (max(altitude.values()) - min(altitude.values())),
                 max(altitude.values()) + 0.05 * (max(altitude.values()) - min(altitude.values()))]
    # Altitude
    fig_alt = go.Figure(go.Scatter(x=list(altitude.keys()),
                                   y=list(altitude.values()),
                                   mode='lines',
                                   hovertemplate='<b>%{text}</b>',
                                   text=[f't = {round(time, 3)} s<br>'
                                         f'y = {round(alt, 3)} m'
                                         for time, alt in altitude.items()],
                                   name='Altitude'))
    # Motor burnout
    fig_alt.add_trace(go.Scatter(x=[burnout, burnout],
                                 y=alt_range,
                                 mode='lines',
                                 name='Burnout'))
    # Chute deploy
    fig_alt.add_trace(go.Scatter(x=[burnout + chute_delay, burnout + chute_delay],
                                 y=alt_range,
                                 mode='lines',
                                 name='Chute deploy'))
    # Apogee
    fig_alt.add_trace(go.Scatter(x=[t_apogee, t_apogee],
                                 y=alt_range,
                                 mode='lines',
                                 name='Apogee'))
    # Set axis ranges
    fig_alt.update_xaxes(range=x_range)
    fig_alt.update_yaxes(range=alt_range)
    # Set titles
    fig_alt.update_layout(title_text='Altitude-time',
                          xaxis_title_text='Time (s)',
                          yaxis_title_text='Altitude (m)')

    # ------------------------------ Velocity ------------------------------
    vel_range = [min(velocity.values()) - 0.05 * (max(velocity.values()) - min(velocity.values())),
                 max(velocity.values()) + 0.05 * (max(velocity.values()) - min(velocity.values()))]
    # Velocity
    fig_vel = go.Figure(go.Scatter(x=list(velocity.keys()),
                                   y=list(velocity.values()),
                                   mode='lines',
                                   hovertemplate='<b>%{text}</b>',
                                   text=[f't = {round(time, 3)} s<br>'
                                         f'v = {round(vel, 3)} m/s'
                                         for time, vel in velocity.items()],
                                   name='Velocity'))
    # Motor burnout
    fig_vel.add_trace(go.Scatter(x=[burnout, burnout],
                                 y=vel_range,
                                 mode='lines',
                                 name='Burnout'))
    # Chute deploy
    fig_vel.add_trace(go.Scatter(x=[burnout + chute_delay, burnout + chute_delay],
                                 y=vel_range,
                                 mode='lines',
                                 name='Chute deploy'))
    # Apogee
    fig_vel.add_trace(go.Scatter(x=[t_apogee, t_apogee],
                                 y=vel_range,
                                 mode='lines',
                                 name='Apogee'))
    # Set axis ranges
    fig_vel.update_xaxes(range=x_range)
    fig_vel.update_yaxes(range=vel_range)
    # Set titles
    fig_vel.update_layout(title_text='Velocity-time',
                          xaxis_title_text='Time (s)',
                          yaxis_title_text=r'$\textsf{Velocity }(\frac{\textsf{m}}{\textsf{s}})$')

    # ------------------------------ Acceleration ------------------------------
    acc_range = [min(acceleration.values()) - 0.05 * (max(acceleration.values()) - min(acceleration.values())),
                 max(acceleration.values()) + 0.05 * (max(acceleration.values()) - min(acceleration.values()))]
    # Acceleration
    fig_acc = go.Figure(go.Scatter(x=list(acceleration.keys()),
                                   y=list(acceleration.values()),
                                   mode='lines',
                                   hovertemplate='<b>%{text}</b>',
                                   text=[f't = {round(time, 3)} s<br>'
                                         f'a = {round(acc, 3)} m/s^2'
                                         for time, acc in acceleration.items()],
                                   name='Acceleration'))
    # Motor burnout
    fig_acc.add_trace(go.Scatter(x=[burnout, burnout],
                                 y=acc_range,
                                 mode='lines',
                                 name='Burnout'))
    # Chute deploy
    fig_acc.add_trace(go.Scatter(x=[burnout + chute_delay, burnout + chute_delay],
                                 y=acc_range,
                                 mode='lines',
                                 name='Chute deploy'))
    # Apogee
    fig_acc.add_trace(go.Scatter(x=[t_apogee, t_apogee],
                                 y=acc_range,
                                 mode='lines',
                                 name='Apogee'))
    # Set axis ranges
    fig_acc.update_xaxes(range=x_range)
    fig_acc.update_yaxes(range=acc_range)
    # Set titles
    fig_acc.update_layout(title_text='Acceleration-time',
                          xaxis_title_text='Time (s)',
                          yaxis_title_text=r'$\textsf{Acceleration }(\frac{\textsf{m}}{\textsf{s}^2})$')

    return fig_alt, fig_vel, fig_acc


def move(t: float, dt: float, F_thrust: float, v: float, y: float, m: float, d: float, Cd: float = None) \
        -> tuple[float, float, float, float]:
    if not Cd:
        F = F_thrust - g * m + calc_drag_force(v, d)
    else:
        F = F_thrust - g * m + calc_drag_force(v, d, Cd)
    a = F / m
    v += a * dt
    y += v * dt
    if y < 0:
        y = 0
        v = 0
    return t + dt, a, v, y


def calc_drag_force(v: float, d: float, Cd=0.5):
    """ F_drag = 0.5 * Cd * ρ * v^2 * A

    https://www.grc.nasa.gov/www/k-12/airplane/drageq.html

    :param v: Velocity
    :param d: Diameter
    :param Cd: Drag coefficient
    :return: The drag force
    """
    direction = 1
    if v > 0:
        direction = -1
    return direction * 0.5 * Cd * 1.205 * (v ** 2) * ((d / 2) ** 2 * math.pi)
