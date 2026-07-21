import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
from road_generator import make_road

# Constants
M1 = 30.0
M2 = 375.0
K1 = 225000.0
K2 = 23550.0
B = 1783.0
G = 9.81
V = 28.0
GAIN = 10

# Make the road. The road variable itself is a function that takes in time and returns height of the road
road = make_road(road_class="C", velocity=V)

def main():
    t_0, t_f, t_res = 0, 16.4, 1000      # Time period to solve for
    z0 = [0.0, 0.0, 0.0, 0.0]           # Initial Conditions

    # Passive motion
    sol_p = solve_ivp(deriv, (t_0, t_f), z0, t_eval=np.linspace(t_0, t_f, t_res), max_step=1e-3, args=(0.0,))
    t = sol_p.t
    x1_p, x2_p, v1_p, v2_p = sol_p.y

    # Skyhook motion
    sol_s = solve_ivp(deriv, (t_0, t_f), z0, t_eval=np.linspace(t_0, t_f, t_res), max_step=1e-3, args=(2175.0,))
    x1_s, x2_s, v1_s, v2_s = sol_s.y

    z = np.array([road(r) for r in t]) # Setup road as an array

    fig, (ax_p, ax_s) = plt.subplots(2, 1)
    plt.subplots_adjust(hspace=0.5)

    # Plot setup
    ax_p.set_ylim(-0.5, 1.5)
    ax_p.set_xlim(-2, 2)
    ax_p.set_title("Passive")
    ax_s.set_ylim(-0.5, 1.5)
    ax_s.set_xlim(-2, 2)
    ax_s.set_title("Skyhook: 0.7 Damping Ratio")

    # Starting heights
    body_start = 0.8
    wheel_start = 0.3
    road_start = 0.0

    # Passive plot components
    body_height_p, = ax_p.plot([], [], linestyle="--",color="orange", alpha=0.5)
    body_box_p = patches.Rectangle((0,0), 0.6, 0.4, fill=False, edgecolor="orange")
    ax_p.add_patch(body_box_p)
    wheel_box_p = patches.Rectangle((0,0), 0.2, 0.2, fill=False, edgecolor="blue")
    ax_p.add_patch(wheel_box_p)
    road_height_p, = ax_p.plot([], [], color="gray")
    road_marker_p, = ax_p.plot([], [], marker="o", color="gray")

    # Skyhook plot components
    body_height_s, = ax_s.plot([], [], linestyle="--", color="orange", alpha=0.5)
    body_box_s = patches.Rectangle((0,0), 0.6, 0.4, fill=False, edgecolor="orange")
    ax_s.add_patch(body_box_s)
    wheel_box_s = patches.Rectangle((0,0), 0.2, 0.2, fill=False, edgecolor="blue")
    ax_s.add_patch(wheel_box_s)
    road_height_s, = ax_s.plot([], [], color="gray")
    road_marker_s, = ax_s.plot([], [], marker="o", color="gray")

    # Update function used in FuncAnimation()
    def update(frame):
        # Set up x-axis to plot full roads
        x_res = 200
        width = int(x_res/2)
        x_axis = np.linspace(-2, 2, x_res)

        # Road will scroll on the screen
        scrolling_road = [(road_start + z[frame-width+i] * GAIN) for i in range(width)] + [(road_start + z[frame+j] * GAIN) for j in range(width)]
        
        # Passive updates
        scrolling_body_p = [(road_start + body_start + x2_p[frame-width+i]*GAIN) for i in range(width)]

        body_height_p.set_data(x_axis[:width], scrolling_body_p)
        body_box_p.set_xy((-0.6/2, road_start + body_start + x2_p[frame]*GAIN - 0.4/2))
        wheel_box_p.set_xy((-0.2/2, road_start + wheel_start + x1_p[frame]*GAIN - 0.2/2))
        
        road_height_p.set_data(x_axis, scrolling_road)
        road_marker_p.set_data([0], [road_start + z[frame]*GAIN])

        # Skyhook updates
        scrolling_body_s = [(road_start + body_start + x2_s[frame-width+i]*GAIN) for i in range(width)]

        body_height_s.set_data(x_axis[:width], scrolling_body_s)
        body_box_s.set_xy((-0.6/2, road_start + body_start + x2_s[frame]*GAIN - 0.4/2))
        wheel_box_s.set_xy((-0.2/2, road_start + wheel_start + x1_s[frame]*GAIN - 0.2/2))

        road_height_s.set_data(np.linspace(-2, 2, x_res), scrolling_road)
        road_marker_s.set_data([0], [road_start + z[frame]*GAIN])

    # Animate
    ani = FuncAnimation(fig, update, frames=len(t)-100, interval=(t_f-t_0)/len(t), repeat=False)

    plt.show()


def deriv(t, y, c_sky): 
    x1, x2, v1, v2 = y
    F_a = -c_sky * v2
    a1 = (K2*(x2 - x1) + B*(v2 - v1) - K1 * (x1 - road(t)) - F_a) / M1
    a2 = (-K2*(x2 - x1) - B*(v2 - v1) + F_a) / M2
    return [v1, v2, a1, a2]


if __name__=="__main__":
    main()

