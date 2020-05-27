import matplotlib.pyplot as plt
import numpy as np

STANDARD_GRAVITY = 9.81  # m s^-2
dt = 0.001


def main():
    pos_0 = np.array([0, 0, 1])
    vel_0 = np.array([1, 5, 10])
    g = np.array([0, 0, -STANDARD_GRAVITY])
    plot_projectile_motion(pos_0, vel_0, g)


def plot_projectile_motion(pos: np.ndarray, vel: np.ndarray, grav: np.ndarray):
    t = 0
    trajectory = [pos]
    y_loc = len(pos) - 1
    while pos[y_loc] > 0:
        vel = vel + grav * dt
        pos = pos + vel * dt
        t += dt
        trajectory.append(pos)

    # TODO: force the grid to be square
    fig = plt.figure()
    if len(pos) == 3:
        for r in range(2):
            for c in range(2):
                ax = fig.add_subplot(2, 2, c + 2 * r + 1, projection='3d')
                ax.plot([p[0] for p in trajectory], [p[1] for p in trajectory], [p[2] for p in trajectory])
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('z')
                if r == 0:
                    if c == 0:
                        ax.view_init(90, 0)
                else:
                    if c == 0:
                        ax.view_init(0, 0)
                    else:
                        ax.view_init(0, 90)
    elif len(pos) == 2:
        ax = fig.add_subplot()
        ax.plot([p[0] for p in trajectory], [p[1] for p in trajectory])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    elif len(pos) == 1:
        ax = fig.add_subplot()
        ax.plot([i * dt for i in range(len(trajectory))], [p[0] for p in trajectory])
        ax.set_xlabel('t')
        ax.set_ylabel('y')
    plt.show()


if __name__ == '__main__':
    main()
