import os
from os import listdir
from os.path import isfile, join
from typing import Dict

import numpy as np
import plotly.graph_objects as go
from dash_html_components import Figure
from scipy.interpolate import interp1d


class ThrustCurve:
    def __init__(self, file_name: str):
        """ The thrust curve.

        :param file_name: The file name including file extension.
        The file extension has to be .eng. E.g. 'Estes_D12.eng'
        """
        if not file_name.endswith('.eng'):
            raise Exception('File should be of type .eng')
        self.file_name = file_name

        self.name = ''
        with open(os.path.join('.', thrust_folder, file_name), 'r') as f:
            file_text = f.read()
            lines = file_text.splitlines()
            lines = [line.strip() for line in lines if line and not line.startswith(';')]
            self.name = lines[0].split()[0]

        file_str = file_name.split('_', 1)[1].split('.')[0].split('_')
        if file_str[-1].isnumeric():
            rec = int(file_str[-1])
            self.name += f' (#{rec + 1})'

        self.manufacturer = file_name.split('_')[0]
        self.thrust_curve = read_thrust_curve(file_name)  # {s, N}
        self.impulse = calc_impulse(list(self.thrust_curve.keys()), list(self.thrust_curve.values()))  # Ns
        self.avg_thrust = calc_average_thrust(list(self.thrust_curve.keys()), list(self.thrust_curve.values()))  # N
        # self.isp_range = ''
        # self.length = -1  # m
        # self.diameter = -1  # m
        # self.type = ''
        # self.dry_mass = -1  # kg
        # self.wet_mass = -1  # kg
        # self.burn_time = -1  # s
        # self.delay = -1  # s
        # self.mass_curve = {}  # s,kg

    def __str__(self):
        return f'{self.manufacturer} {self.name}'

    def thrust_curve_smooth(self, dt: float):
        return spline_thrust_curve(self.thrust_curve, dt)


def get_thrust_curve_plot(thrust_curve: Dict[float, float], avg_thrust: float = None, title: str = '') -> Figure:
    """ Plots the thrust curve. The file name is used to make a title to the graph. """

    t = list(thrust_curve.keys())
    f = list(thrust_curve.values())
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=t,
                             y=f,
                             mode='lines',
                             hovertemplate='<b>%{text}</b>',
                             text=[f't = {round(time, 3)} s<br>F = {round(force, 3)} N' for time, force in zip(t, f)],
                             showlegend=False))

    x_range = [-0.025 * max(t), 1.025 * max(t)]
    if avg_thrust:
        fig.add_trace(go.Scatter(x=x_range,
                                 y=[avg_thrust, avg_thrust],
                                 mode='lines',
                                 name='Average thrust'))

    fig.update_layout(title_text=title,
                      xaxis_title_text='Time (s)',
                      yaxis_title_text='Thrust (N)')
    fig.update_xaxes(range=x_range)
    return fig


def read_thrust_curve(file_name: str) -> Dict[float, float]:
    """ Converts the raw thrust curve data file to a dictionary. """
    if file_name not in thrust_files:
        raise FileNotFoundError(f'{file_name} does not exist in the directory "{thrust_folder}"')

    with open(os.path.join('.', thrust_folder, file_name), 'r') as f:
        file_text = f.read()
        thrust_curve = read_eng_thrust_curve(file_text)

    if 0 not in thrust_curve.keys():
        thrust_curve[0] = 0

    tc = {}
    for k in sorted(thrust_curve):
        tc[k] = thrust_curve[k]

    return tc


def read_eng_thrust_curve(text: str) -> Dict[float, float]:
    """Converts the raw thrust curve .eng data file to a dictionary.

    :param text: The raw data from the file
    :return: A dictionary with the times as keys and the corresponding thrust as the value
    """
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line and not line.startswith(';')]
    lines = lines[1:]

    times = [float(line.split(' ')[0].split('\t')[0]) for line in lines]
    thrusts = [float(line.split(' ')[-1].split('\t')[-1]) for line in lines]

    return dict(zip(times, thrusts))


def calc_average_thrust(times: list, thrusts: list) -> float:
    """ Uses trapezoid integral approximation to find the average thrust.

    :param times: The times at which the measurements have been made.
    :param thrusts: The thrusts corresponding to the time at the same index.
    :return: The average thrust.
    """
    return calc_impulse(times, thrusts) / max(times)


def calc_impulse(times: list, thrusts: list) -> float:
    """ Uses trapezoid integral approximation to calculate the impulse.

    :param times: The times at which the measurements have been made.
    :param thrusts: The thrusts corresponding to the time at the same index.
    :return: The impulse.
    """
    area = 0

    for i in range(len(times) - 1):
        area += (times[i + 1] - times[i]) * ((thrusts[i + 1] + thrusts[i]) / 2)

    return area


def spline_thrust_curve(thrust_curve: Dict[float, float], dt: float) -> Dict[float, float]:
    """Smooths/interpolates the thrust curve using a cubic spline function.

    :param thrust_curve: The thrust curve to smooth.
    :param dt: The size of the interpolated time steps. In seconds.
    :return: The smoothed thrust curve.
    """
    x = np.array(list(thrust_curve.keys()))
    y = np.array(list(thrust_curve.values()))
    f = interp1d(x, y, kind='slinear')
    x_new = np.linspace(0, max(x), num=int(max(x) / dt))
    values = f(x_new)
    return dict(zip(x_new, values))


thrust_folder = 'thrustcurve'
thrust_files = [f for f in listdir(thrust_folder) if isfile(join(thrust_folder, f)) and f.endswith('.eng')]
motor_names = [str(ThrustCurve(n)) for n in thrust_files]

# I'm keeping this for if I do someday to also allow these file types.
#
# def read_rse_thrust_curve(text: str) -> Dict[float, float]:
#     """Converts the raw thrust curve .rse data file to a dictionary.
#
#     :param text: The raw data from the file
#     :return: A dictionary with the times as keys and the corresponding thrust as the value
#     """
#     lines = text.splitlines()
#     data_start = lines.index('<data>')
#     data_end = lines.index('</data>')
#     data = lines[data_start + 1:data_end]
#
#     times = [find_rse_time(line) for line in data]
#     thrusts = [find_rse_thrust(line) for line in data]
#
#     return dict(zip(times, thrusts))
#
#
# def find_rse_time(line: str) -> float:
#     """Extracts the time component out of a data line of a .rse file.
#
#     :param line: The line from the file that contains the data
#     :return: The time that is specified in that line
#     """
#     time_str = line[line.find('t='):]
#     time_str = time_str[time_str.find("\"") + 1:]
#     time_str = time_str[:time_str.find("\"")]
#     return float(time_str)
#
#
# def find_rse_thrust(line: str) -> float:
#     """Extracts the thrust component out of a data line of a .rse file.
#
#     :param line: The line from the file that contains the data
#     :return: The thrust that is specified in that line
#     """
#     time_str = line[line.find('f='):]
#     time_str = time_str[time_str.find("\"") + 1:]
#     time_str = time_str[:time_str.find("\"")]
#     return float(time_str)
#
#
# def read_edx_thrust_curve(text: str) -> Dict[float, float]:
#     """Converts the raw thrust curve .edx data file to a dictionary.
#
#     :param text: The raw data from the file
#     :return: A dictionary with the times as keys and the corresponding thrust as the value
#     """
#     lines = text.splitlines()
#     lines = [line.split(':')[-1] for line in lines if 'Time /Thrust' in line]
#
#     times = [value.strip().split(' ')[0] for value in lines]
#     times = [float(time) for time in times]
#
#     thrusts = [value.strip().split(' ')[-1] for value in lines]
#     thrusts = [lbf_to_N(float(thrust)) for thrust in thrusts]
#
#     return dict(zip(times, thrusts))
#
#
# def lbf_to_N(lbf: float) -> float:
#     """Converts pound-force to newtons.
#
#     :param lbf: Force in pound-force
#     :return: Force in newtons
#     """
#     return lbf * 4.4482216
#
#
# def read_txt_thrust_curve(text: str) -> Dict[float, float]:
#     """Converts the raw thrust curve .txt data file to a dictionary.
#
#     :param text: The raw data from the file
#     :return: A dictionary with the times as keys and the corresponding thrust as the value
#     """
#     lines = text.splitlines()
#     lines = [line.strip() for line in lines if line and not line.startswith(';')]
#     lines = lines[1:-1]
#
#     times = [float(line.split('\t')[0]) for line in lines]
#     thrusts = [float(line.split('\t')[-1]) for line in lines]
#
#     return dict(zip(times, thrusts))
