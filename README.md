# README
----
## Boids Flocking Simulation

This project is a Python-based simulation of the flocking behavior of birds, commonly referred to as "boids". It is inspired by the algorithm described by Craig Reynolds on his page: [Boids - Flocks, Herds, and Schools: A Distributed Behavioral Model](https://www.red3d.com/cwr/boids/).

----

### Concept of Flocking

Flocking is the behavior exhibited when a group of birds, known as a flock, are foraging or in flight. This natural phenomenon is characterized by the breathtaking patterns and formations that emerge. Craig Reynolds' "Boids" program simulates such flocks with simple steering behaviors. Each boid is an autonomous object that adheres to a set of steering rules which aim to avoid crowding neighbors (separation), steer towards average heading of neighbors (alignment), and steer toward average position of neighbors (cohesion).

----

### Design Choices

1. **Double Buffering**: In order to avoid any inconsistency during simulation, the code uses double buffering; meaning that it first calculates the new states for all the boids, and only when all new states are known, they are applied to the boids.

2. **Toroidal space**: The boids move in a toroidal space, i.e., an area that is topologically equivalent to a torus. It means that the space wraps around both horizontally and vertically - a boid leaving the screen on one side comes back from the opposite side.

3. **Vectorized Calculations**: The code utilizes NumPy for vectorized calculations which is an efficient way to perform large array operations and is faster compared to native Python loops.

4. **Dynamic Adjustments**: You can dynamically adjust the relative importance of alignment, cohesion, and separation behaviors using sliders. This can lead to a rich set of emergent behaviors.

5. **Random Noise**: The acceleration of each boid is injected with a bit of random noise, this adds an element of unpredictability mimicking more closely real-world flocking behavior.

----

### Dependencies

- Python 3.x
- Pygame
- Numpy

You can install the required packages using pip:

```sh
pip install -r requirements.txt
```

---
### How to run

After you have Python and the dependencies installed, simply run the script using Python:

```sh
python run.py
```

This will open a window with the simulation running. You will see boids moving around in a flock. On the top-left corner, you will see sliders that allow you to change the weights for alignment, cohesion, and separation. There's also a restart button to restart the simulation with the current settings.

Feel free to experiment with different settings and observe how the flocking behavior changes.