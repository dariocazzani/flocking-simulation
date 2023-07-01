import pygame
import numpy as np
import random

def set_magnitude(vector:np.ndarray, magnitude:float) -> np.ndarray:
    normalized_vector = vector / np.linalg.norm(vector)
    scaled_vector = normalized_vector * magnitude
    return scaled_vector


class Boid:
    def __init__(self, screen_height:int=1000, screen_width:int=1000) -> None:
        self.s_heigh = screen_height
        self.s_width = screen_width
        self.position = np.array([random.uniform(0, screen_width), random.uniform(0, screen_height)])
        self.velocity = np.random.randn(2) * 4
        self.acceleration = np.array([0.0, 0.0])
        self.max_force:float = 0.2
        self.perception:float = 100
        
    def update(self) -> None:
        self.position += self.velocity
        self.velocity += self.acceleration
        
    def edges(self) -> None:
        if self.position[0] > self.s_width:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = self.s_width
        if self.position[1] > self.s_heigh:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = self.s_heigh
            
        
    def _align(self, boids:list['Boid']) -> np.ndarray:
        other_velocities = []
        for other in boids:
            if self != other and \
                np.linalg.norm(self.position - other.position) < self.perception:
                other_velocities.append(other.velocity)
        steering = np.mean(np.array(other_velocities), axis=0) if len (other_velocities) > 0 else np.zeros_like(self.velocity)
        return set_magnitude(steering - self.velocity, self.max_force)
    
    def flock(self, boids) -> None:
        alignment = self._align(boids)
        self.acceleration = alignment
    
    def show(self, screen):
        # pygame.draw.circle(surface, color, position, radius)
        color:tuple = (255, 255, 255)
        radius:float = 10
        pygame.draw.circle(
            screen,
            color,
            list(self.position),
            radius)


