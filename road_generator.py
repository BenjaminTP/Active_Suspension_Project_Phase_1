import numpy as np
import matplotlib.pyplot as plt

def main():
    t_0, t_f = 0, 3                     # Set up time span
    t = np.linspace(t_0, t_f, 3000)
    v = 30                              # Velocity

    road = make_road(road_class="C", velocity=v)    # Generate the road
    
    # Plotting
    fig, ax1 = plt.subplots()
    ax1.plot(t, road(t), label="road", color="gray")
    ax1.set_ylim(-.2,.2)
    ax1.set_ylabel("Road Height (m)")
    ax1.set_xlabel("Time (s)")
    ax1.legend()
    plt.show()


def make_road(road_class="C", velocity=30.0):
    # Set seed for random number generator for reproducibility
    rng = np.random.default_rng(seed=41)
    # Pick Gd(n0) according to road class
    Gd_n0 = 1e-6 * {"A":16, "B":64, "C":256, "D":1024, "E":4096, "F":16384, "G":65536, "H":262144}[road_class] 

    n_0, w, N = 0.1, 2.0, 1000                          # Set Gd(n) parameters
    n_i, n_f = 10e-3, 2.0                               # Set range of frequencies to sum over. Refer to derivation chart

    n = np.linspace(n_i, n_f, N)                        # Set up range of frequencies
    dn = n[1] - n[0]                                    # Find dn
    A = np.sqrt(2.0 * Gd_n0 * (n/n_0) ** (-w) * dn)     # Find the amplitude of each frequency
    phi = rng.uniform(0, 2*np.pi, N)                    # Randomize a set of phase shifts, phi

    # We want to return a function that holds the road height for any position, so we simply return a that, a function
    def generate(x):
        road_height = 0
        for i in range(len(n)):
            road_height += A[i] * np.sin(2 * np.pi * n[i] * x * velocity + phi[i])  # Sum all the waves
        return road_height
    
    return generate


if __name__=="__main__":
    main()