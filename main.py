import math
import os

import matplotlib.pyplot as plt
import numpy as np

STANDARD_GRAVITY = 9.80665  # m s^-2
dt = 0.001


def main():
    # pos_0 = np.array([0, 0, 1])
    # vel_0 = np.array([1, 5, 10])
    # g = np.array([0, 0, -STANDARD_GRAVITY])
    # projectile_motion(pos_0, vel_0, g)

    engines = ['Estes_C6_1.eng', 'Cesaroni_O25000']
    for engine in engines:
        thrust_curve = read_thrust_curve(engine)
        plot_thrust_curve(thrust_curve, engine)


def read_thrust_curve(file_name: str) -> dict:
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


def read_eng_thrust_curve(text: str) -> dict:
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line and not line.startswith(';')]
    lines = lines[1:]

    times = [float(line.split(' ')[0]) for line in lines]
    thrusts = [float(line.split(' ')[-1]) for line in lines]

    thrust_curve = dict(zip(times, thrusts))

    return thrust_curve


def read_rse_thrust_curve(text: str) -> dict:
    lines = text.splitlines()
    data_start = lines.index('<data>')
    data_end = lines.index('</data>')
    data = lines[data_start + 1:data_end]

    times = [find_rse_time(line) for line in data]
    thrusts = [find_rse_thrust(line) for line in data]

    thrust_curve = dict(zip(times, thrusts))

    return thrust_curve


def find_rse_time(line: str) -> float:
    time_str = line[line.find('t='):]
    time_str = time_str[time_str.find("\"") + 1:]
    time_str = time_str[:time_str.find("\"")]
    return float(time_str)


def find_rse_thrust(line: str) -> float:
    time_str = line[line.find('f='):]
    time_str = time_str[time_str.find("\"") + 1:]
    time_str = time_str[:time_str.find("\"")]
    return float(time_str)


def read_edx_thrust_curve(text: str) -> dict:
    return {}


def read_txt_thrust_curve(text: str) -> dict:
    return {}


def plot_thrust_curve(thrust_curve: dict, file_name: str):
    fig = plt.figure()
    ax = fig.add_subplot()

    t = list(thrust_curve.keys())
    f = list(thrust_curve.values())

    ax.plot(t, f)

    average_thrust = calc_average_thrust(t, f)
    ax.plot([0, math.ceil(max(t) * 4) / 4], [average_thrust, average_thrust], '--')

    ax.set_title(file_name[:-4].replace('_', ' ', 1).replace('_', '-', 1))
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Thrust (N)')
    ax.set_xlim(0, math.ceil(max(t) * 4) / 4)
    ax.set_ylim(0, round(max(f) * 1.1))
    ax.grid()

    fig.show()


def calc_average_thrust(times: list, thrusts: list) -> float:
    """ Uses trapezoid integral approximation to find the average thrust """
    area = 0

    for i in range(len(times) - 1):
        area += (times[i + 1] - times[i]) * ((thrusts[i + 1] + thrusts[i]) / 2)

    return area / max(times)


def projectile_motion(pos: np.ndarray, vel: np.ndarray, gravity: np.ndarray, plot=True):
    t = 0
    trajectory = [pos]
    y_loc = len(pos) - 1
    while pos[y_loc] > 0:
        vel = vel + gravity * dt
        pos = pos + vel * dt
        t += dt
        trajectory.append(pos)

    if plot:
        plot_trajectory(trajectory, len(pos))

    return trajectory


def plot_trajectory(trajectory, dimensions):
    fig = plt.figure()
    if dimensions == 3:
        x = [p[0] for p in trajectory]
        y = [p[1] for p in trajectory]
        z = [p[2] for p in trajectory]
        axis_limits = calc_axis_limits(x, y, z)
        for r in range(2):
            for c in range(2):
                ax = fig.add_subplot(2, 2, c + 2 * r + 1, projection='3d')
                ax.plot(x, y, z)
                ax.set_xlabel('x (m)')
                ax.set_ylabel('y (m)')
                ax.set_zlabel('Altitude (m)')
                ax.set_xlim3d(axis_limits[0][0], axis_limits[0][1])
                ax.set_ylim3d(axis_limits[1][0], axis_limits[1][1])
                ax.set_zlim3d(axis_limits[2][0], axis_limits[2][1])
                if r == 0:
                    if c == 0:
                        ax.view_init(90, 0)
                else:
                    if c == 0:
                        ax.view_init(0, 0)
                    else:
                        ax.view_init(0, 90)
    elif dimensions == 2:
        ax = fig.add_subplot()
        x = [p[0] for p in trajectory]
        y = [p[1] for p in trajectory]
        ax.plot(x, y)
        ax.set_xlabel('x (m)')
        ax.set_ylabel('Altitude (m)')
        ax.axis('equal')
    elif dimensions == 1:
        ax = fig.add_subplot()
        t = [i * dt for i in range(len(trajectory))]
        y = [p[0] for p in trajectory]
        ax.plot(t, y)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Altitude (m)')
    plt.show()


def calc_axis_limits(x, y, z):
    x_range = max(x) - min(x)
    y_range = max(y) - min(y)
    z_range = max(z) - min(z)

    max_range = max(x_range, y_range, z_range)

    if x_range < max_range:
        extension = (max_range - x_range) / 2
        x_limits = (min(x) - extension, max(x) + extension)
    else:
        x_limits = (min(x), max(x))

    if y_range < max_range:
        extension = (max_range - y_range) / 2
        y_limits = (min(y) - extension, max(y) + extension)
    else:
        y_limits = (min(y), max(y))

    if z_range < max_range:
        extension = (max_range - z_range)
        z_limits = (min(z), max(z) + extension)
    else:
        z_limits = (min(z), max(z))

    return x_limits, y_limits, z_limits


if __name__ == '__main__':
    main()
