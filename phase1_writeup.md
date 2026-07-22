# Phase 1

For phase 1, these were the overarching tasks that I will go through:

1. Deriving the equations of motion 
2. Researching and choosing variables for the passive system
3. Simulating the passive system
4. Simulating the system with skyhook controls
5. Generating ISO8608 standard roads and integrating these roads into the skyhook simulations
6. Running a full test bench to see the improvements
7. Animating passive vs. active systems

# 1. Deriving the EOM

I originally looked up the classic derivation of the system, however was unsatisfied by the lack of explanation as to why gravity could be ignored, and some hand waving that most tutorials showed. So I decided to derive them from first principles.

Here is the FBD for the derivation:
![Free Body Diagram](phase1_writeup_images/FBD.png)
*Note that the FBDs on the right show the forces when the masses are moving upward. The directions of the force change depending on direction of motion. Also note that each mass does have gravity acting downward, but the vector is not drawn in.*

The damper force $F_2$ is simply proportional to the velocity of the masses:

$$
F_2=b(\dot{x}_2-\dot{x}_1)
$$

Take the absolute coordinates of the masses as $X_1, X_2$ and the unstretched/compressed lengths of the springs to be $l_1, l_2$. From this we can derive the spring forces. Forces on mass 2 are:

$$
F_1=k_2(X_2-X_1-l_2)\\

m_2\ddot{x}_2=-F_1-F_2-m_2g\\

m_2\ddot{x}_2=-k_2(X_2-X_1-l_2)-F_2-m_2g\\ \ \\
$$

At Equilibrium:

$$
\ddot{x}_2=\dot{x}_2=\dot{x}_1=0,\  X_2=X_{2,eq},\ X_1=X_{1,eq}\\ \ \\

\Rightarrow m_2g=-k_2(X_{2,eq}-X_{1,eq}-l_2) \\ \ \\

$$

Now if the system is in motion, $X_2=X_{2,eq}+x_2,\ X_1=X_{1,eq}+x_1$, which is just saying some deviation from equilibrium. From here, we know the system is in motion, so acceleration and velocities are back:

$$
m_2\ddot{x}_2=-k_2((X_{2,eq}+x_2)-(X_{1,eq}+x_1)-l_2)-F_2-m_2g\\ 

m_2\ddot{x}_2=-k_2(X_{2,eq}-X_{1,eq}-l_2+x_2-x_1)-F_2-m_2g\\ 

m_2\ddot{x}_2=-k_2(X_{2,eq}-X_{1,eq}-l_2)-k_2(x_2-x_1)-F_2-m_2g\\ \ \\

m_2g=-k_2(X_{2,eq}-X_{1,eq}-l_2),\ (From\ Above) \\ \Rightarrow m_2\ddot{x}_2=\cancel{-k_2(X_{2,eq}-X_{1,eq}-l_2)}-k_2(x_2-x_1)-F_2\cancel{-m_2g}\\

\therefore m_2\ddot{x}_2=-k_2(x_2-x_1)-b(\dot{x}_2-\dot{x}_1)
$$

If we also take into account that the road is moving, we can write absolute coordinate of it as $X_r$. The forces on mass one are:

$$
F_1=k_2(X_2-X_1-l_2)\\

F_3=k_1(X_1-X_r-l_1)\\

m_1\ddot{x}_1=k_2(X_2-X_1-l_2)+F_2-k_1(X_1-X_r-l_1)-m_1g\\
$$

At equilibrium: $\ddot{x}_1=\dot{x}_1=\dot{x}_2=0$, and $X_1=X_{1,eq}, X_2=X_{2,eq}, X_r=X_{r,eq}$

$$
k_2(X_{2,eq}-X_{1,eq}-l_2)-k_1(X_{1,eq}-X_{r,eq}-l_1)=m_1g
$$

In motion, velocities and accelerations are back, and $X_1=X_{1,eq}+x_1, X_2=X_{2,eq}+x_2, X_r=X_{r,eq}+x_r$. From here we can solve:

$$
m_1\ddot{x}_1=k_2((X_{2,eq}+x_2)-(X_{1,eq}+x_1)-l_2)+F_2-k_1((X_{1,eq}+x_1)-(X_{r,eq}+x_r)-l_1)-m_1g \\ \ \\

m_1\ddot{x}_1=k_2(X_{2,eq}-X_{1,eq}-l_2+x_2-x_1)+F_2-k_1(X_{1,eq}-X_{r,eq}-l_1+x_1-x_r)-m_1g \\ \ \\

m_1\ddot{x}_1=k_2(X_{2,eq}-X_{1,eq}-l_2)+k_2(x_2-x_1)+F_2-k_1(X_{1,eq}-X_{r,eq}-l_1)-k_1(x_1-x_r)-m_1g
$$

From earlier:

$$
k_2(X_{2,eq}-X_{1,eq}-l_2)-k_1(X_{1,eq}-X_{r,eq}-l_1)=m_1g\\ \ \\

\Rightarrow m_1\ddot{x}_1=\cancel{k_2(X_{2,eq}-X_{1,eq}-l_2)}+k_2(x_2-x_1)+F_2\cancel{-k_1(X_{1,eq}-X_{r,eq}-l_1)}-k_1(x_1-x_r)\cancel{-m_1g}\\ \ \\

\therefore m_1\ddot{x}_1=k_2(x_2-x_1)+b(\dot{x}_2-\dot{x}_1)-k_1(x_1-x_r)
$$

The final equations of motion are:

$$
m_1\ddot{x}_1=k_2(x_2-x_1)+b(\dot{x}_2-\dot{x}_1)-k_1(x_1-x_r)\\

m_2\ddot{x}_2=-k_2(x_2-x_1)-b(\dot{x}_2-\dot{x}_1)
$$

It is worth noting that each $x_1, x_2, x_r$ is measured from the equilibrium position, as that is how we got the cancellations of $m_1g$ and $m_2g$.

#  2.Finding the Parametes $m_1, m_2, k_1, k_2$ and $b$
Earlier we derived these equations of motion:

$$
m_1\ddot{x}_1=k_2(x_2-x_1)+b(\dot{x}_2-\dot{x}_1)-k_1(x_1-x_r)\\

m_2\ddot{x}_2=-k_2(x_2-x_1)-b(\dot{x}_2-\dot{x}_1)
$$

We need to choose the parameters $m_1, m_2, k_1, k_2$, and $b$.

### Finding Mass

Using the average weight of a decent car (1500kg), and taking a quarter of that gives us $m_2$ of 375kg. 

Looking at average wheel weights, I found 30kg to be within the average, giving us our $m_1$.

$$\therefore m_1=30kg, m_2=375kg$$

### Finding Spring Stiffness

$k_1$ is simply the tire stiffness, so we can look for average stiffness of a tire. Results show they typically range from 150-300 kN/m, so let’s pick something in the middle of 225 kN/m.

According to *Fundamentals of Vehicle Dynamics* by Gillespie, the average car will range in natural frequency from 1-1.5Hz, so we will be going with $f_n=1.2Hz$. This natural frequency has shown to be a comfortable ride for passengers, and it reduces vibrations for anything above the $\sqrt{2}\times f_n \approx 1.7Hz$. 

For our calculations we need our frequency in rad/s:

$$
\omega_n=2\pi f_n=7.54 rad/s
$$

Also from Gillespie, we know that ride rate is: $RR=\frac{k_1k_2}{k_1+k_2}$(both springs in series) and $\omega_n=\sqrt{\frac{RR}{m_2}}$, literally just $f_n=\frac{1}{2\pi}\sqrt{\frac{k}{m}}$. We can find $k_2$ like this:

$$
\omega_n=\sqrt{\frac{RR}{m_2}} \Rightarrow RR=m_2\omega_n^2\\

RR=\frac{k_1k_2}{k_1+k_2} \Rightarrow \frac{k_1k_2}{k_1+k_2}=m_2\omega_n^2\\ \ \\

k_1k_2=m_2\omega_n^2(k_1+k_2)\\

k_1k_2=m_2\omega_n^2k_1+m_2\omega_n^2k_2\\

k_1k_2-m_2\omega_n^2k_2=m_2\omega_n^2k_1\\

k_2(k_1-m_2\omega_n^2)=m_2\omega_n^2k_1\\

k_2=\frac{m_2\omega_n^2k_1}{k_1-m_2\omega_n^2}
$$

Substituting in $m_w, w_n$, and $k_1$ gives us the two spring stiffnesses:

$$
k_1=225000N/m\\
k_2=23550N/m
$$

### Finding $b$

The suspension damping ratio (marked as $\zeta_s$) on modern passenger cars usually falls between 0.2 and 0.4, so we will go with $\zeta_s=0.3$ (Gillespie, pg.148).

From Gillespie, we also get $\zeta_s=\frac{b}{2\sqrt{k_2m_2}}$. We can now solve for our damping coefficient:

$$
b=2\zeta_s\sqrt{k_2m_2}=1783N\cdot s/m
$$

### Checking Natural Frequencies

Using the equation for natural frequency we can check what they are for each spring-mass system:

$$
f_n=\frac{1}{2\pi}\sqrt{\frac{k}{m}}\\ \ \\

f_{n,2}=\frac{1}{2\pi}\sqrt{\frac{RR}{m_2}}=1.2Hz\\

f_{n,1}=\frac{1}{2\pi}\sqrt{\frac{k_1+k_2}{m_1}}=14.50Hz
$$

According to Gillespie, $f_{n,2}$ should be between 1-1.5Hz, and we have hit that. Gillespie also gives a range of 10-15Hz for $f_{n,1}$ which we have also hit.

The $RR$ and $k_1+k_2$ in the place of normally just the $k_i$ value seems to come out of nowhere, however, for the second mass, when moving, it makes sense that both springs are applying a force in series on the mass. Try to just imagine pressing down on the second mass, they act in series.

For mass one, the springs are attached on both sides, meaning they create a chain, and since the mass is between the springs, the system acts as if it were in parallel. Imagine the force of each spring as the mass moves to either side, they act in parallel.

# 3. Passive Baseline Sim
https://github.com/BenjaminTP/Active-Suspension-Project/blob/main/passive_sim.py

This link is to the that will solve the EOM, and return $x_1(t), x_2(t), v_1(t)$ and $v_2(t)$ given some initial conditions and an equation for the road, $x_r(t)$. 

The sim will then plot the motion of body and wheel, as well as the body acceleration like across time:


![passive_cos_bump.png](Images/passive_cos_bump.png)*Cosine bump in the road*

![passive_2cm_push_down.png](Images/passive_2cm_push_down.png)*Hold and release body 20cm down*

Finally, the sim calculates the body’s frequency, RMS body acceleration, and peak body acceleration.

Notice that the body frequency is around 1.175Hz, 2.1% off from the hand calculated 1.2Hz. One note on the body frequency is that it is different depending on the road and speed, however, the 1.17Hz is accurate because it is the frequency when just simply pushing and releasing the body.

# 4. Adding Skyhook Controls

### Hand Calcs

The passive baseline will still have oscillations, but we want to dampen those completely. This is where active suspension comes in. We will compensate the motion with an actuator.

From the EOM, we can add a force $F_a$ as an internal force pair:

$$
m_1\ddot{x}_1=k_2(x_2-x_1)+b(\dot{x}_2-\dot{x}_1)-k_1(x_1-x_r) - F_a\\

m_2\ddot{x}_2=-k_2(x_2-x_1)-b(\dot{x}_2-\dot{x}_1)+F_a
$$

Summing the EOM will show that those forces end up cancelling as expected.

The way skyhook works, is that it imagines a damper attached to the sky and directly dampens the movement of $m_2$.

$$
F_a=-c_{sky}\cdot\dot{x}_2
$$

We want to get close to critically damping $m_2$, and to do that we need to find $c_c$ (critical damping coefficient) as such:

$$
c_c=2\sqrt{km}\\ 

\Rightarrow c_c=2\sqrt{\frac{k_1k_2m_2}{k_1+k_2}}
$$

Using our previously derived parameters, we find:

$$
c_c=2\sqrt{\frac{(225000)(23550)(375)}{225000+23550}}=5655N\cdot s/m
$$

Knowing this, we can tweak our numbers to get a total damping ratio $(\zeta_{effective})$ of 0.7, as per textbook damping rules:

$$
\zeta_{effective}\cdot c_c=3958N\cdot s/m\\

\therefore c_{sky}=3958-b=2175N\cdot s/m\\
$$

We can also find our force required from the actuator, which will be:

$$
F_a(t)=-2175\cdot \dot{x}_2(t)
$$

To find the peak force, we know this will come when $\dot{x}_2$ is at its peak. For anything moving in a sinusoidal pattern ($x(t)=A\sin(\omega t + \phi)$, where $A$ is amplitude, and $\omega$ is frequency in rad/s), the peak can be found by taking the derivative: 

$$
x(t)=A\sin(\omega t+\phi) \Rightarrow \dot{x}(t)=A\omega\cos(\omega t+\phi)
$$

We know the peak of $\cos(t)$ will always be 1, so the actual peak must be $A\omega$. We also know that the largest movements will come at resonance $f_n$, which is 1.2Hz from when we picked the parameters. Assuming a body amplitude of 20mm, we know that the peak velocity will be:

$$
f_{n,2}=1.2Hz\\

\Rightarrow \omega_{n,2}=1.2\cdot2\pi=7.54rad/s\\

\dot{x}_{peak}=0.151m/s\\ \ \\

\therefore \lvert F_{peak} \rvert=328.4N
$$

From $F_{peak}$, we can size out an actuator that will work.

### Adding Skyhook to the Sim

https://github.com/BenjaminTP/Active-Suspension-Project/blob/main/skyhook_sim.py

This sim is essentially the same as the passive sim, however, we add $F_a$ into the deriv function:

```python
C_SKY = 2175

def deriv(t, y): 
    x1, x2, v1, v2 = y
    F_a = -C_SKY * v2
    a1 = (K2*(x2 - x1) + B*(v2 - v1) - K1 * (x1 - road(t)) - F_a) / M1
    a2 = (-K2*(x2 - x1) - B*(v2 - v1) + F_a) / M2
    return [v1, v2, a1, a2]
```

The plotting and calculations are the same as the passive sim.

![skyhook_cos_bump_2175.png](Images/skyhook_cos_bump_2175.png)*Cosine bump with 0.7 effective damping ratio*

![skyhook_2cm_push_down_2175.png](Images/skyhook_2cm_push_down_2175.png)*Hold and release 20cm down with 0.7 effective damping ratio*

![skyhook_cos_bump_3972.png](Images/skyhook_cos_bump_3972.png)*Cosine bump with 1.0 effective damping ratio*

![skyhook_2cm_push_down_3972.png](Images/skyhook_2cm_push_down_3972.png)*Hold and release 20cm down with 1.0 effective damping ratio*

Compare these plots and results to the plots of the passive baseline:


![passive_cos_bump.png](Images/passive_cos_bump.png)*Passive baseline: cosine bump in the road*

![passive_2cm_push_down.png](Images/passive_2cm_push_down.png)*Passive baseline: hold and release body 20cm down*

Clearly the skyhook controls dampen the movements a lot. The RMS and peak body acceleration also drops too.

# 5. Adding ISO8608 Road Profiles

### What is the ISO8608 standard?

The core idea is that any road can be represented as a sum of waves using the FFT; FFT will just decompose the shape of the road into a sum of sine waves. We can represent the data as the Power Spectral Density (PSD), represented as $G_d(n)$, which is a plot of the rate of power for each frequency in the waves from the FFT. 

The interesting bit is that when plotting $G_d(n)$ from real data on a log-log graph, the road data kept following this straight line trend with slope of -2. This is how the ISO8608 standard was born, and from this, we can classify road types as by following this graph:

![Displacement PSD vs. Spatial Frequency](phase1_writeup_images/ISO8608_classes_plot.png)

Looking at this chart, we can see that the frequency domain is $n\in[10^{-2},2]$, which will become useful when picking which frequencies to generate the road from. The full equation of the line is:

$$
G_d(n)=G_d(n_0)\left(\frac{n}{n_0}\right)^{-w}
$$

Where $n_0$ is typically 0.1 cycles/meter, and $w$ is 2. Notice that this equation can be rearranged as:

$$
G_d(n)=\frac{G_d(n_0)}{n_0^{-w}}\cdot n^{-w} \Rightarrow G_d(n) \propto n^{-w}
$$

Which is a simple polynomial saying that the PSD for some frequency is proportional to that frequency raised to some power, typically -2. This is a beautiful result.

To classify a road according to the classes A-H, in the ISO8608 standard, we can classify a road based purely on $G_d(n_0)$. The reason this works is because our road data will follow the same $w=-2$ trend, so the only thing differing each straight line is an intercept, which has conventionally been chosen to be $G_d(n_0=0.1cycles/m)$

As for the meaning of the classes themselves, A is a very smooth road, and each road is rougher than the last. For our simulation, we will be using class C since it is an extreme on average roads.

| Class | Gd(n0) (e-6 m³) | Band (e-6 m³) | Feels like |
| --- | --- | --- | --- |
| A | 16 | < 32 | new motorway |
| B | 64 | 32–128 | good paved road |
| C | 256 | 128–512 | worn road |
| D | 1024 | 512–2048 | poor, patched road |
| E | 4096 | 2048–8192 | bad gravel |
| F–H | 16384 / 65536 / 262144 | up to > 131072 | tracks, off-road misery |

### How to generate a road

Ok this is all cool, but how do we even generate a road profile from this information, and how do we make sure it is a class we want?

One thing that threw me off in this derivation is that each wave carries with it some power, which is actually the same thing as variance. To get terminology correct, the curve $G_d(n)$ is the rate of power with respect to a frequency. In other words, $\frac{power(n_i)}{dn}=G_d(n_i)$. To get back this power, we simply do this: $power(n_i)=G_d(n_i)\cdot dn$. Since we are using a discrete slice, $power(n_i)=G_d(n_i)\triangle n$.

We the work with the variance (AKA power) of an arbitrary sine wave, which can be derived as such:

$$
Var(A\cdot\sin(\omega t + \phi))\equiv\frac{1}{T}\int_0^T(A\cdot\sin(\omega t +\phi))^2dt\\ \ \\
=\frac{1}{T}\int_0^TA^2\sin^2(\omega t+\phi)dt\\
u=\omega t +\phi \Rightarrow\frac{1}{T}\int_0^TA^2\sin^2(\omega t+\phi)dt=\frac{A^2}{T}\cdot\int_\phi^{\omega T +\phi}\sin^2(u)\frac{1}{\omega} du\\
=\frac{A^2}{T\omega}\cdot\int_\phi^{\omega T +\phi} \sin^2(u)du\\
=\frac{A^2}{T\omega} \cdot\left[ \frac{u}{2}-\frac{\sin(2u)}{4} \right]_\phi^{\omega T +\phi}\\
=\frac{A^2}{2\omega T} \cdot\left[ u-\frac{\sin(2u)}{2}\right]_\phi^{\omega T +\phi}\\
=\frac{A^2}{2\omega T}\cdot\left[ \omega T\cancel{+\phi}-\frac{\sin(2\omega T+2\phi)}{2} \cancel{-\phi}+\frac{\sin(2\phi)}{2} \right]\\
=\frac{A^2}{2\omega T}\cdot\left[ \omega T-\frac{\sin(2\omega T+2\phi)-\sin(2\phi)}{2}\right]\\
T=\frac{2\pi}{\omega} \Rightarrow =\frac{A^2}{4\pi}\cdot\left[ 2\pi-\frac{\sin(4\pi+2\phi)-\sin(2\phi)}{2}\right]\\
=\frac{A^2}{4\pi}\cdot\left[ 2\pi-\frac{\cancel{\sin(4\pi)\cos(2\phi)}+\cancel{\cos(4\pi)}\sin(2\phi)-\sin(2\phi)}{2}\right]\\
=\frac{A^2}{4\pi}\cdot\left[ 2\pi-\frac{\cancel{\sin(2\phi)}\cancel{-\sin(2\phi)}}{2}\right]\\
=\frac{A^2}{4\pi}\cdot2\pi\\
\therefore Var(A\cdot\sin(\omega t + \phi))=\frac{A^2}{2}
$$

Since power and variance are the same thing, we can follow up with:

$$
power(n_i)=G_d(n_i)\triangle n, Var(A\cdot \sin(\omega t+\phi))=\frac{A^2}{2}\\ \ \\
Var(A\cdot\sin(\omega t+\phi))=power(n_i)\Rightarrow \frac{A_i^2}{2}=G_d(n_i)\triangle n\\
A_i=\sqrt{2G_d(n_i)\triangle n}
$$

This it the formula that we need, an amplitude for some frequency $n_i$. From here, we can construct every wave $(f(x))$, as a function of amplitude, frequency, and a phase shift:

$$
f(x)=A_i\cdot\sin(2\pi n_ix+\phi_i)
$$

The phase shift here is a random number, such that $\phi_i \in [0,2\pi]$. We need to add a random phase shift to each wave, so they are not completely in sync. Think about a crowd clapping, if they all clap together then it is not a good model of clapping, instead shift their phases by a random amount and suddenly we have a proper model. Same logic will apply to roads.

To actually sum all the waves we need to simply add them up as such to get height of the road as a function of time:

$$
z(x)=\sum_i A_i\cdot\sin(2\pi n_ix+\phi_i)
$$

## Code

### Road Generator/Visualizer

https://github.com/BenjaminTP/Active-Suspension-Project/blob/main/road_generator.py

In terms of code, we can create a road generating function:

```python
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
```

One part we have not yet discussed is velocity, which is very important for the road generator. Without velocity, the function that is returned takes in meters, but we need to know where the road is at a certain time. To do this, we simply multiply by the velocity of the car. This turns the units into seconds, and now we can take in time as a parameter instead of distance.

After that we can simply generate our road, then plot it over all time to visualize the road.

```python
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

```

This code yields a plot of the road that we can see: 

![Seed 40 road](phase1_writeup_images/Seed40_road.png)
*Seed=40*

![Seed 41 road](phase1_writeup_images/Seed41_road.png)
*Seed=41*

![Seed 42 road](phase1_writeup_images/Seed42_road.png)
*Seed=42*

![Seed 43 road](phase1_writeup_images/Seed43_road.png)
*Seed=43*

### Using the Road Generator in the Main Sim

https://github.com/BenjaminTP/Active-Suspension-Project/blob/main/skyhook_sim_ISO8608_road.py

Using the skyhook sim from earlier, we can integrate the road generator. One major issue was that our acceleration data was off because the road generated below the wheel starting position, causing the body to accelerate violently. We solved this by just ignoring the first 0.5s for acceleration data.

Here are the results on a class C roads that span 400m:

#### Seed=41, Speed=100km/hr
![100kph_seed41_passive.png](Images/100kph_seed41_passive.png)
*Passive*

![100kph_seed41_skyhook_2175.png](Images/100kph_seed41_skyhook_2175.png)
*Skyhook: damping ratio=0.7*

![100kph_seed41_skyhook_3972.png](Images/100kph_seed41_skyhook_3972.png)
*Skyhook: damping ratio=1.0*

#### Seed=42, Speed=100km/hr

![100kph_seed42_passive.png](Images/100kph_seed42_passive.png)
*Passive*

![100kph_seed42_skyhook_2175.png](Images/100kph_seed42_skyhook_2175.png)
*Skyhook: damping ratio=0.7*

#### Seed=43, Speed=100km/hr

![100kph_seed43_passive.png](Images/100kph_seed43_passive.png)
*Passive*

![100kph_seed43_skyhook_2175.png](Images/100kph_seed43_skyhook_2175.png)
*Skyhook: damping ratio=0.7*

#### Seed=41, Speed=50km/hr

![50kph_seed41_passive.png](Images/50kph_seed41_passive.png)
*Passive*

![50kph_seed41_skyhook_2175.png](Images/50kph_seed41_skyhook_2175.png)
*Skyhook: damping ratio=0.7*

We can now simulate real roads according to the ISO8608 standard, and see the improvements to comfort (RMS accel.).

# 6. Full Test Bench

All the sims I have been building so far are great and all, but useless unless we do a lot of testing. For example, we could keep reducing the RMS body acceleration, but there will always be tradeoffs, however, what are those tradeoffs?

The three major tradeoffs are the peak suspension travel $\max(\lvert x_2-x_1\rvert)$, peak tire deflection $\max(\lvert x_1 - x_r \rvert)$, and peak actuator force $\max(\lvert c_{sky}\cdot\dot{x}_2 \rvert)$. These matter, because they govern the dimensions and of tires, suspension, and actuators. These are very easy to implement into the sim that we have https://github.com/BenjaminTP/Active-Suspension-Project/blob/main/full_testing_benchmark.py. Here are the test cases and results:

### Test 1
![Test 1](Images/test1.png)
*Class-C Road, Passive, Start at Rest*

RMS Body Acceleration: 1.675 m/s^2
Peak Body Acceleration: 7.043 m/s^2
Peak Suspension Travel: 38.230mm
Peak Tire Deflection: 15.126mm
Peak Actuator Force: 0.0N

### Test 2
![Test 2](Images/test2.png)
*Class-C Road, Skyhook (0.7), Start at Rest*

RMS Body Acceleration: 1.515 m/s^2
Peak Body Acceleration: 5.761 m/s^2
Peak Suspension Travel: 31.288mm
Peak Tire Deflection: 14.333mm
Peak Actuator Force: 466.8N

### Test 3
![Test 3](Images/test3.png)
*5cm Bump Road, Passive, Start at Rest*

RMS Body Acceleration: 0.970 m/s^2
Peak Body Acceleration: 4.948 m/s^2
Peak Suspension Travel: 38.676mm
Peak Tire Deflection: 8.945mm
Peak Actuator Force: 0.0N

### Test 4
![Test 4](Images/test4.png)
*5cm Bump Road, Skyhook (0.7), Start at Rest*

RMS Body Acceleration: 0.851 m/s^2
Peak Body Acceleration: 4.902 m/s^2
Peak Suspension Travel: 41.561mm
Peak Tire Deflection: 8.780mm
Peak Actuator Force: 559.0N

### Test 5
![Test 5](Images/test5.png)
*Flat Road, Passive, Start Body 8cm Down*

RMS Body Acceleration: 0.955 m/s^2
Peak Body Acceleration: 5.024 m/s^2
Peak Suspension Travel: 80.000mm
Peak Tire Deflection: 9.445mm
Peak Actuator Force: 0.0N

### Test 6
![Test 6](Images/test6.png)
*Flat Road, Skyhook (0.7), Start Body 8cm Down*

RMS Body Acceleration: 0.596 m/s^2
Peak Body Acceleration: 3.810 m/s^2
Peak Suspension Travel: 78.954mm
Peak Tire Deflection: 8.782mm
Peak Actuator Force: 663.2N

### Test 7
![Test 7](Images/test7.png)
*Resonating Road, Passive, Start at Rest*

RMS Body Acceleration: 0.870 m/s^2
Peak Body Acceleration: 1.233 m/s^2
Peak Suspension Travel: 17.139mm
Peak Tire Deflection: 2.111mm
Peak Actuator Force: 0.0N

### Test 8
![Test 8](Images/test8.png)
*Resonating Road, Skyhook (0.7), Start at Rest*

RMS Body Acceleration: 0.373 m/s^2
Peak Body Acceleration: 0.528 m/s^2
Peak Suspension Travel: 9.334mm
Peak Tire Deflection: 0.926mm
Peak Actuator Force: 155.6N

## Reduction Percentages

| **Road** | **RMS Accel.** | **Peak Accel.** | **Susp. Travel** | **Tire Deflect.** |
| --- | --- | --- | --- | --- |
| Class C | -9.6% | -18.2% | -18.2% | -5.2% |
| 5cm Bump | -12.3% | -0.9% | **+7.5%** | -1.8% |
| Flat (Body released from 8cm down) | -37.6% | -24.2% | -1.3% | -7.0% |
| Resonance Road | -57.1% | -57.2% | -45.6% | -56.1% |

From this we can clearly see that there is a significant improvement in comfort (RMS Accel.) between passive and skyhook control. All of this is happening while suspension travel and tire deflection are almost always improved as well, on top of the comfort and peak accel (all except 5cm bump suspension travel).

# 7. Animating Passive vs. Active Systems

# My Animation

https://github.com/BenjaminTP/Active-Suspension-Project/blob/main/animation.py

I wrote up an animation sim linked above. This shows how the body (orange), wheel (blue), and road (grey) move over time. On top is the passive system, and the bottom shows the active variation.

![Class-C Road Gif](Images/classC_road.gif)
*Class-C road*

![Resonance Road Gif](Images/resonance_road.gif)
*Resonance Road*

Notice the big difference that skyhook control adds here. This truly visualizes the calcs we have been doing all along.

## Interactive Sim (Claude)

Having never touched animations before, especially with python or HTML, I instructed Claude to take the parameters and calculations I have to build out a more visually appealing version of the simulation, while adding an interactive layer on top, so you are able to draw the road. This is not my work, but it uses my calculations to create a nicer animation.

https://github.com/BenjaminTP/Active-Suspension-Project/blob/main/claude_animation.html

# Concluding Remarks

There are many different types of active suspension systems, and I only implemented skyhook controls. There are other things I want to add onto the sim, but due to time constraints, I could not do more without sacrificing phase 2. 

Phase 2 will implement a preview control system on top of skyhook into the physical model. I will go back to phase 1 and implement the preview control after hitting my personal deadline for phase 2. 
