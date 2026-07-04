import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Generate Particles and arrays to contain X, Y coordinates
particles = random.randint(10, 50)

print(f"Creating: {particles} particles")

particle_x = np.random.rand(particles)
particle_y = np.random.rand(particles)

vel_x = (np.random.rand(particles) - 0.5) * 0.02
vel_y = (np.random.rand(particles) - 0.5) * 0.02
# Setup figure and axes

fig, ax = plt.subplots(figsize=(8,8))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

ax.set_title("Ideal Gas / Molecular Diffusion simulation")

point, = ax.plot([], [], "ro", color="#1f77b4")
# Create animation

def animate(frame):
    global particle_x, particle_y, vel_x, vel_y

    # Update positions using velocities
    particle_x += vel_x
    particle_y += vel_y

    # Vecorize boundaries, if they hit wall flip direction
    hit_wall_x = (particle_x <= 0) | (particle_x >= 1)
    vel_x[hit_wall_x] *= -1

    hit_wall_y = (particle_y <= 0) | (particle_y >= 1)
    vel_y[hit_wall_y] *= -1

    # update plot
    point.set_data(particle_x, particle_y)
    return point

    return point

ani = animation.FuncAnimation(fig, animate, frames=200, interval=100, repeat=False)
plt.show()