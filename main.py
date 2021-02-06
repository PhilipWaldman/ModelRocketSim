from typing import List, Tuple, Dict

import matplotlib.pyplot as plt
import numpy as np

STANDARD_GRAVITY = 9.80665  # m s^-2
dt = 0.001


def main():
    # plt.xkcd()  # LOL
    example_thrust_curve_reading()
    # example_projectile_motion()


def powered_flight(thrust_curve: Dict[float, float], pos: np.ndarray, vel: np.ndarray, facing: np.ndarray, mass: float,
                   plot: bool = True) -> List[np.ndarray]:
    """ Calculates the trajectory the object will take when under powered flight.

    :param thrust_curve:
    :param pos: Initial position vector
    :param vel: Initial velocity vector
    :param facing:
    :param mass:
    :param plot: When True, plots the trajectory, otherwise only returns it
    :return: List of position vectors where the object will be
    """
    t = 0
    trajectory = [pos]
    while t <= max(thrust_curve.keys()):
        pass

    if plot:
        plot_trajectory(trajectory)
    return trajectory


def projectile_motion(pos: np.ndarray, vel: np.ndarray, plot: bool = True) -> List[np.ndarray]:
    """ Calculates the trajectory the object will take when not under powered flight.

    :param pos: Initial position vector
    :param vel: Initial velocity vector
    :param plot: When True, plots the trajectory, otherwise only returns it
    :return: List of position vectors where the object will be
    """
    gravity = np.array([0, 0, -STANDARD_GRAVITY])
    t = 0
    trajectory = [pos]
    while pos[-1] > 0:
        pos, vel = move(pos, vel, gravity)
        t += dt
        trajectory.append(pos)

    if plot:
        plot_trajectory(trajectory)
    return trajectory


def move(pos: np.ndarray, vel: np.ndarray, acc: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    new_vel = vel + acc * dt
    new_pos = pos + vel * dt
    return new_pos, new_vel


def plot_trajectory(trajectory: List[np.ndarray]) -> None:
    """ Plots the trajectory of positions in 1-, 2-, and 3-D.

    :param trajectory: List of position vectors the object
    """
    fig = plt.figure()
    dimensions = len(trajectory[0])
    if dimensions == 3:
        x = [p[0] for p in trajectory]
        y = [p[1] for p in trajectory]
        z = [p[2] for p in trajectory]
        axis_limits = calc_3D_axis_limits(x, y, z)
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
                ax.set_proj_type('ortho')
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


def calc_3D_axis_limits(x: List[float], y: List[float], z: List[float]) -> \
        Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
    """Calculates the axis limits of a 3D plot to make the x-, y-, and z-axes equally scaled.

    :param x: The x values to be plotted
    :param y: The y values to be plotted
    :param z: The z values to be plotted
    :return: The limits for the x-, y-, and z-axes
    """
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


def example_projectile_motion():
    """ An example demonstrating the projectile_motion method """
    pos_0 = np.array([0, 0, 1])
    vel_0 = np.array([1, 5, 10])
    projectile_motion(pos_0, vel_0)


def example_thrust_curve_reading():
    """ An example demonstrating thrust curve reading """
    import thrust_curves as tc
    engines = ['AeroTech_G8', 'Cesaroni_O25000']
    for engine in engines:
        try:
            thrust_curve = tc.read_thrust_curve(engine)
            tc.plot_thrust_curve(thrust_curve, engine)
        except FileNotFoundError:
            print('The entered file does not exist in the thrustcurve folder. Make sure you have not made any typos.')


if __name__ == '__main__':
    main()
