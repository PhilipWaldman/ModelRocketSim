import os
from os import listdir
from os.path import isfile, join
from typing import Dict

import plotly.graph_objects as go
from dash_html_components import Figure


class ThrustCurve:
    def __init__(self, file_name: str):
        """ The thrust curve.

        :param file_name: The file name including file extension.
        The file extension has to be .eng. E.g. 'Estes_D12.eng'
        """
        # TODO: load thrust curves with API
        # https://www.thrustcurve.org/info/api.html
        # https://www.thrustcurve.org/info/apidemo.html
        # Read more info from file
        # https://www.thrustcurve.org/info/raspformat.html
        if not file_name.endswith('.eng'):
            raise Exception('File should be of type .eng')
        self.file_name = file_name

        with open(os.path.join('.', thrust_folder, file_name), 'r') as f:
            file_text = f.read()
            lines = file_text.splitlines()
            lines = [line.strip() for line in lines if line and not line.startswith(';')]
            header_line = lines[0].split()

            # self.name = header_line[0]
            if file_name.split('_')[1] == 'Micro':
                self.name = 'Micro Maxx'
            elif file_name.split('_')[1] == '1':
                self.name = '/'.join(file_name.split('_')[1:]).split('.')[0]
            else:
                self.name = file_name.split('_')[1].split('.')[0]
            self.diameter = int(float(header_line[1]))  # mm
            self.length = float(header_line[2])  # mm
            self.delays = [int(d) if type(d) == 'int' else d for d in header_line[3].split('-')]
            self.prop_mass = float(header_line[4])  # kg
            self.wet_mass = float(header_line[5])  # kg
            self.dry_mass = self.wet_mass - self.prop_mass  # kg

        self.manufacturer = map_manufacturer(file_name.split('_')[0])
        self.thrust_curve = read_thrust_curve(file_name)  # {s, N}
        self.impulse = calc_impulse(self.thrust_curve, 2)  # Ns
        self.avg_thrust = calc_average_thrust(self.thrust_curve, 2)  # N
        self.burn_time = calc_burn_time(self.thrust_curve, 2)  # s
        self.impulse_range = ''
        # self.mass_curve = {}  # s,kg

    def plot(self):
        return get_thrust_curve_plot(self.thrust_curve, self.avg_thrust, str(self))

    def __str__(self):
        return f'{self.manufacturer} {self.name}'


def map_manufacturer(name: str) -> str:
    mapping = {'AeroTech': 'AeroTech',
               'AMW': 'Animal Motor Works',
               'Apogee': 'Apogee Components',
               'Cesaroni': 'Cesaroni Technology',
               'Contrail': 'Contrail Rockets',
               'Estes': 'Estes Industries',
               'Hypertek': 'Hypertek',
               'KBA': 'Kosdon by AeroTech',
               'Loki': 'Loki Research',
               'Quest': 'Quest Aerospace',
               'RATT': 'R.A.T.T. Works',
               'Klima': 'Raketenmodellbau Klima',
               'SCR': 'Southern Cross Rocketry'}
    if name in mapping.keys():
        return mapping[name]
    return name


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
    if 'thrust_files' in locals() and file_name not in thrust_files or \
            'thrust_curves' in locals() and file_name not in [c.file_name for c in thrust_curves]:
        raise FileNotFoundError(f'{file_name} does not exist in the directory "{thrust_folder}"')

    with open(os.path.join('.', thrust_folder, file_name), 'r') as f:
        file_text = f.read()
        thrust_curve = read_eng_thrust_curve(file_text)

    if 0 not in thrust_curve.keys():
        thrust_curve[0] = 0

    tc = {k: thrust_curve[k] for k in sorted(thrust_curve)}

    return tc


def read_eng_thrust_curve(text: str) -> Dict[float, float]:
    """ Converts the raw thrust curve .eng data file to a dictionary.

    :param text: The raw data from the file
    :return: A dictionary with the times as keys and the corresponding thrust as the value
    """
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line and not line.startswith(';')]
    lines = lines[1:]

    times = [float(line.split(' ')[0].split('\t')[0]) for line in lines]
    thrusts = [float(line.split(' ')[-1].split('\t')[-1]) for line in lines]

    return dict(zip(times, thrusts))


def calc_average_thrust(thrust_curve: Dict[float, float], ndigits: int = None) -> float:
    """ Uses trapezoid integral approximation to find the average thrust.

    :param thrust_curve: The thrust curve.
    :param ndigits: The number of digits to round to. Default: does not round.
    :return: The average thrust.
    """
    tc = get_5_percent_thrust_range(thrust_curve)
    impulse = calc_impulse(tc)
    dt = calc_burn_time(tc)
    if dt == 0:
        impulse = calc_impulse(thrust_curve)
        dt = max(thrust_curve.keys())
    thrust = impulse / dt
    return round(thrust, ndigits) if ndigits else thrust


def calc_burn_time(thrust_curve: Dict[float, float], ndigits: int = None) -> float:
    """ Calculates the burn time of the motor.

    :param thrust_curve: The thrust curve.
    :param ndigits: The number of digits to round to. Default: does not round.
    :return: The burn time of the motor in seconds.
    """
    tc = get_5_percent_thrust_range(thrust_curve)
    t = max(tc.keys()) - min(tc.keys())
    return round(t, ndigits) if ndigits else t


def get_5_percent_thrust_range(thrust_curve: Dict[float, float]) -> Dict[float, float]:
    """ Removes the thrusts where the thrust is <= 5% of the max thrust.

    :param thrust_curve: The thrust curve.
    :return: The thrust curve where every thrust value is > 5% of the max thrust.
    """
    # TODO: interpolate tc to smaller time steps in case of big time steps / thrust changes at start and end.
    max_thrust = max(thrust_curve.values())
    threshold = max_thrust * 0.05
    valid_thrust_curve = {}
    for t, F in thrust_curve.items():
        if F > threshold:
            valid_thrust_curve[t] = F
    return valid_thrust_curve


def interpolate_thrust_curve(thrust_curve: Dict[float, float], dt: float = 0.01) -> Dict[float, float]:
    pass


def calc_impulse(thrust_curve: Dict[float, float], ndigits: int = None) -> float:
    """ Uses trapezoid integral approximation to calculate the impulse.

    :param thrust_curve: The thrust curve.
    :param ndigits: The number of digits to round to. Default: does not round.
    :return: The impulse.
    """
    times = list(thrust_curve.keys())
    thrusts = list(thrust_curve.values())

    area = 0
    for i in range(len(times) - 1):
        area += (times[i + 1] - times[i]) * ((thrusts[i + 1] + thrusts[i]) / 2)
    return round(area, ndigits) if ndigits else area


thrust_folder = 'thrustcurve'
thrust_files = [f for f in listdir(thrust_folder) if isfile(join(thrust_folder, f)) and f.endswith('.eng')]

thrust_curves = [ThrustCurve(f) for f in thrust_files]
# thrust_curve_df = pd.DataFrame({
#     'thrust_curve': [tc for tc in thrust_curves],
#     'diameter': [tc.diameter for tc in thrust_curves],
#     'length': [tc.length for tc in thrust_curves],
#     'manufacturer': [tc.manufacturer for tc in thrust_curves],
#     'impulse': [tc.impulse for tc in thrust_curves],
#     'avg_thrust': [tc.avg_thrust for tc in thrust_curves],
#     'burn_time': [tc.burn_time for tc in thrust_curves],
#     'impulse_range': [tc.impulse_range for tc in thrust_curves]
# })
