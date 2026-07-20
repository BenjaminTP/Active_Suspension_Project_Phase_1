import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Constants
M1 = 30.0
M2 = 375.0
K1 = 225000.0
K2 = 23550.0
B = 1783.0
C_SKY = 2175
G = 9.81


def main():
    t_0, t_f = 0, 3 # Time period to solve for
    z0 = [0.0, 0.0, 0.0, 0.0] # Initial Conditions

    sol = solve_ivp(deriv, (t_0, t_f), z0, t_eval=np.linspace(t_0, t_f, 500), max_step=1e-3) # Solve the ODE
    
    # Extract solutions
    t = sol.t
    x1, x2, v1, v2 = sol.y
    a2 = (K2 * (x1 - x2) + B * (v1 - v2) - C_SKY * v2) / M2

    # Solve body frequency, RMS body accel., and peak body accel.
    freq2 = solve_freq(x2, t)
    rms_a2 = np.sqrt(np.mean(a2**2))
    print("---------------- Results ----------------")
    print(f"Body Frequency: {freq2:.3f} Hz")
    print(f"RMS Body Acceleration: {rms_a2:.3f} m/s^2, or {(rms_a2/G):.3f} g's")
    print(f"Peak Body Accleration: {np.max(np.abs(a2)):.3f} m/s^2, or or {(np.max(np.abs(a2))/G):.3f} g's")
    print("-----------------------------------------")

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1)
    plt.subplots_adjust(hspace=0.5)

    ax1.plot(t, x1 * 1000, label="x1") # *1000 to put in mm
    ax1.plot(t, x2 * 1000, label="x2")
    ax1.plot(t, [road(r)*1000 for r in t], label="road", color="gray", linestyle="--")
    ax2.plot(t, a2, label="a2", color="r")

    ax1.set_ylabel("Height from Equil. (mm)")
    ax2.set_ylabel("Body Accel. (m/s^2)")
    ax2.set_xlabel("Time (s)")

    ax1.set_title(f"Body Frequency: {freq2:.3f} Hz")
    ax2.set_title(f"RMS Body Acceleration: {rms_a2:.3f} m/s^2)\n Peak Body Accleration: {np.max(np.abs(a2)):.3f} m/s^2")

    ax1.grid(alpha=0.25)
    ax2.grid(alpha=0.25)

    ax1.legend()
    ax2.legend()

    fig.tight_layout()
    
    # Plot saving
    filename = input("Filename: ")
    if filename not in ["skip", "pass", "no", "exit", "test"]:
        plt.savefig(f"images/{filename}", dpi=150)

    plt.show()


# Feed this into solve_ivp. 
# Essentially you need t and y as parameters, and the function needs to return dy/dt.
# Using dy/dt, solve_ivp will step and find the original function y.

def deriv(t, y): 
    x1, x2, v1, v2 = y
    F_a = -C_SKY * v2
    a1 = (K2*(x2 - x1) + B*(v2 - v1) - K1 * (x1 - road(t)) - F_a) / M1
    a2 = (-K2*(x2 - x1) - B*(v2 - v1) + F_a) / M2
    return [v1, v2, a1, a2]


# Road height as a function of time
def road(t):
    # t0, t1, H = 0.5, 0.7, 0.05
    # if t0 <= t and t <= t1:
    #     return 0.5 * H * (1 - np.cos(2 * np.pi * (t - t0) / (t1 - t0)))
    return 0.0


def solve_freq(pos, t):
    # Populate an array with times where the position passes zero
    cross_times = []
    i_last = 0
    for i in range(1, len(pos)):
        if pos[i] > 0 and pos[i_last] < 0 or pos[i] < 0 and pos[i_last] > 0: # Where pos crosses 0, store that time
            cross_times.append(t[i])
        i_last = i

    # Add up the differences between cross times and find the mean
    diff = 0
    for j in range(1, len(cross_times)):
        diff += cross_times[j]-cross_times[j-1] # Calculate difference
    mean = diff / (len(cross_times) - 1)
    try:
        return 1/(2*mean) # mean is avg time to cross 0 -> a wave crosses twice a period -> frequency = 1/period
    except ZeroDivisionError:
        return 0


if __name__=="__main__":
    main()