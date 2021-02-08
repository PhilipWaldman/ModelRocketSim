import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import thrust_curve as tc
from app import app

layout = html.Div([
    html.H3('Thrust curve'),
    dcc.Dropdown(
        id='thrust-curve-dropdown',
        options=[{'label': m, 'value': f} for m, f in zip(tc.motor_names, tc.thrust_files)],
        value=tc.thrust_files[0]),
    # TODO: Add sliders to set ranges
    # dcc.RangeSlider(
    #     id='thrust-slider',
    #     min=0,
    #     max=20,
    #     step=0.5,
    #     value=[5, 15]
    # )
    dcc.Graph(id='thrust-curve')
],
    style={
        'margin-left': '2rem',
        'margin-right': '2rem'
    }
)


@app.callback(
    Output('thrust-curve', 'figure'),
    Input('thrust-curve-dropdown', 'value'))
def plot_thrust_curve(file_name):
    if file_name is None:
        return go.Figure()
    thrust_curve = tc.ThrustCurve(file_name)
    return thrust_curve.get_thrust_curve_plot()
