import os
from typing import Dict

import matplotlib.pyplot as plt


def read_thrust_curve(file_name: str) -> Dict[float, float]:
    """Converts the raw thrust curve data file to a dictionary.

    :param file_name: The name of the thrust curve file
    :return: A dictionary with the times as keys and the corresponding thrust as the value
    """
    file_exists = False
    for dirname, _, filenames in os.walk(os.path.join('.', 'thrustcurve')):
        for filename in filenames:
            if file_name in filename:
                file_exists = True
                break
    if not file_exists:
        raise FileNotFoundError

    if '.' not in file_name:
        for dirname, _, filenames in os.walk(os.path.join('.', 'thrustcurve')):
            for filename in filenames:
                if file_name in filename:
                    file_name = filename
                    break

    with open(os.path.join('.', 'thrustcurve', file_name), 'r') as f:
        file_text = f.read()
        if file_name.endswith('eng'):
            thrust_curve = read_eng_thrust_curve(file_text)
        elif file_name.endswith('rse'):
            thrust_curve = read_rse_thrust_curve(file_text)
        elif file_name.endswith('edx'):
            thrust_curve = read_edx_thrust_curve(file_text)
        elif file_name.endswith('txt'):
            thrust_curve = read_txt_thrust_curve(file_text)

    return thrust_curve


def read_eng_thrust_curve(text: str) -> Dict[float, float]:
    """Converts the raw thrust curve .eng data file to a dictionary.

    :param text: The raw data from the file
    :return: A dictionary with the times as keys and the corresponding thrust as the value
    """
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line and not line.startswith(';')]
    lines = lines[1:]

    times = [float(line.split(' ')[0]) for line in lines]
    thrusts = [float(line.split(' ')[-1]) for line in lines]

    return dict(zip(times, thrusts))


def read_rse_thrust_curve(text: str) -> Dict[float, float]:
    """Converts the raw thrust curve .rse data file to a dictionary.

    :param text: The raw data from the file
    :return: A dictionary with the times as keys and the corresponding thrust as the value
    """
    lines = text.splitlines()
    data_start = lines.index('<data>')
    data_end = lines.index('</data>')
    data = lines[data_start + 1:data_end]

    times = [find_rse_time(line) for line in data]
    thrusts = [find_rse_thrust(line) for line in data]

    return dict(zip(times, thrusts))


def find_rse_time(line: str) -> float:
    """Extracts the time component out of a data line of a .rse file.

    :param line: The line from the file that contains the data
    :return: The time that is specified in that line
    """
    time_str = line[line.find('t='):]
    time_str = time_str[time_str.find("\"") + 1:]
    time_str = time_str[:time_str.find("\"")]
    return float(time_str)


def find_rse_thrust(line: str) -> float:
    """Extracts the thrust component out of a data line of a .rse file.

    :param line: The line from the file that contains the data
    :return: The thrust that is specified in that line
    """
    time_str = line[line.find('f='):]
    time_str = time_str[time_str.find("\"") + 1:]
    time_str = time_str[:time_str.find("\"")]
    return float(time_str)


def read_edx_thrust_curve(text: str) -> Dict[float, float]:
    """Converts the raw thrust curve .edx data file to a dictionary.

    :param text: The raw data from the file
    :return: A dictionary with the times as keys and the corresponding thrust as the value
    """
    lines = text.splitlines()
    lines = [line.split(':')[-1] for line in lines if 'Time /Thrust' in line]

    times = [value.strip().split(' ')[0] for value in lines]
    times = [float(time) for time in times]

    thrusts = [value.strip().split(' ')[-1] for value in lines]
    thrusts = [lbf_to_N(float(thrust)) for thrust in thrusts]

    return dict(zip(times, thrusts))


def lbf_to_N(lbf: float) -> float:
    """Converts pound-force to newtons.

    :param lbf: Force in pound-force
    :return: Force in newtons
    """
    return lbf * 4.4482216


def read_txt_thrust_curve(text: str) -> Dict[float, float]:
    """Converts the raw thrust curve .txt data file to a dictionary.

    :param text: The raw data from the file
    :return: A dictionary with the times as keys and the corresponding thrust as the value
    """
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line and not line.startswith(';')]
    lines = lines[1:-1]

    times = [float(line.split('\t')[0]) for line in lines]
    thrusts = [float(line.split('\t')[-1]) for line in lines]

    return dict(zip(times, thrusts))


def plot_thrust_curve(thrust_curve: Dict[float, float], file_name: str) -> None:
    """Plots the thrust curve. The file name is used to make a title to the graph.

    :param thrust_curve: A thrust curve dictionary
    :param file_name: The name of the file the thrust curve came from
    """
    fig = plt.figure()
    ax = fig.add_subplot()

    t = list(thrust_curve.keys())
    f = list(thrust_curve.values())

    ax.plot(t, f)

    average_thrust = calc_average_thrust(t, f)
    ax.plot([0, round(max(t) * 4 * 1.1) / 4], [average_thrust, average_thrust], '--')

    if '.' in file_name:
        file_name = file_name.split('.')[0]
    ax.set_title(file_name.replace('_', ' ', 1).replace('_', '-', 1))
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Thrust (N)')

    ax.set_xlim(0, round(max(t) * 4 * 1.1) / 4)
    ax.set_ylim(0, round(max(f) * 1.1))
    ax.grid()

    fig.show()


def calc_average_thrust(times: list, thrusts: list) -> float:
    """Uses trapezoid integral approximation to find the average thrust."""
    area = 0

    for i in range(len(times) - 1):
        area += (times[i + 1] - times[i]) * ((thrusts[i + 1] + thrusts[i]) / 2)

    return area / max(times)
