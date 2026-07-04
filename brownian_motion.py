import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from pyparsing import alphas

# Constants

k_B = 1.38064852e-23 # Boltzmann constant
dt = 0.05            # Time step
num_steps = 200

# Initial physical parameters
init_T = 300 # Kelvin
init_eta = 1.0 # Dynamic viscosity
init_r = 1.0 # Particle radius (micrometers)

# setup figure and subplots
fig, ax = plt.subplots(figsize=(8,8))
plt.subplots_adjust(bottom=0.3)

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_title('Brownian Motion')
ax.grid(True, linestyle='--', alpha=0.5)

# initialize trace and particle elements
line, = ax.plot([], [], lw=1.5, color="#1f77b4")
point, = ax.plot([],[], "ro", ms=12)

# Global variable to hold generated path
x, y = np.zeros(num_steps), np.zeros(num_steps)

def generate_path(T, eta, r):
    """Calculates step scaling and outputs a new random walk path"""
    actual_eta = eta * 1e-3
    actual_r = r * 1e-6

    # Eistein-stokes diffusion coefficient
    D = (k_B * T) / (6 * np.pi * actual_eta * actual_r)
    step_scale = np.sqrt(2 * D * dt) * 1e6

    # generate cumulitive coordinates
    dx = np.random.normal(0, step_scale, num_steps)
    dy = np.random.normal(0, step_scale, num_steps)
    return np.cumsum(dx), np.cumsum(dy)

# Generate initial path
x, y = generate_path(init_T, init_eta, init_r)

ax_T = plt.axes([0.15, 0.18, 0.65, 0.03])
ax_eta = plt.axes([0.15, 0.12, 0.65, 0.03])
ax_r = plt.axes([0.15, 0.06, 0.65, 0.03])

# Define sliders
slider_T = Slider(ax_T, "Temp (K)", 100, 500, valinit=init_T, valfmt="%0.0f K")
slider_eta = Slider(ax_eta, "Viscosity", 0.1, 10.0, valinit=init_eta, valfmt="%0.1f (Water=1)")
slider_r = Slider(ax_r, "Radius (µm)", 0.2, 5.0, valinit=init_r, valfmt="%0.1f µm")

def update_sliders(val):
    """Triggers whenever slider moves: generates a new path based on new physics"""
    global x,y
    x, y = generate_path(slider_T.val, slider_eta.val, slider_r.val)

# Attach update logic to sliders
slider_T.on_changed(update_sliders)
slider_eta.on_changed(update_sliders)
slider_r.on_changed(update_sliders)

def animate(frame):
    """Standard loop mapping arrays to screen coordinates"""
    line.set_data(x[:frame], y[:frame])
    point.set_data([x[frame]], [y[frame]])
    return line, point

ani = animation.FuncAnimation(fig, animate, frames=num_steps, interval=30, blit=True)
plt.show()