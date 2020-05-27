import matplotlib.pyplot as plt
import numpy as np

STANDARD_GRAVITY = 9.80665  # m s^-2
dt = 0.001


def main():
    pos_0 = np.array([0, 0, 1])
    vel_0 = np.array([1, 5, 10])
    g = np.array([0, 0, -STANDARD_GRAVITY])
    projectile_motion(pos_0, vel_0, g)


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
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('z')
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
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.axis('equal')
    elif dimensions == 1:
        ax = fig.add_subplot()
        ax.plot([i * dt for i in range(len(trajectory))], [p[0] for p in trajectory])
        ax.set_xlabel('t')
        ax.set_ylabel('y')
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
