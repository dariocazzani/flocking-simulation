import pygame
import numpy as np
import random

def set_magnitude(vector:np.ndarray, magnitude:float) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm < 1e-3:
        return vector
    normalized_vector = vector / np.linalg.norm(vector)
    scaled_vector = normalized_vector * magnitude
    return scaled_vector

def average_heading(vectors:np.ndarray) -> np.ndarray:
    sum_vector = np.sum(vectors, axis=0)
    heading = sum_vector / np.linalg.norm(sum_vector)  
    return heading

def average_position(vectors:np.ndarray) -> np.ndarray:
    return np.mean(vectors, axis=0)

def limit_magnitude(vector: np.ndarray, max_magnitude: float) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm < 1e-3:
        return vector  
    if norm > max_magnitude:
        normalized_vector = vector / norm
        scaled_vector = normalized_vector * max_magnitude
        return scaled_vector
    else:
        return vector


class Boid:
    def __init__(self, screen_height:int, screen_width:int) -> None:
        self.s_heigh = screen_height
        self.s_width = screen_width
        self.position = np.array([random.uniform(0, screen_width), random.uniform(0, screen_height)])
        self.velocity = np.random.randn(2) * 2
        self.acceleration = np.array([0.0, 0.0])
        self.max_force:float = 0.5
        self.perception:float = 50
        self.max_speed:float = 5
        
    def update(self) -> None:
        self.position += self.velocity
        self.velocity += self.acceleration
        self.velocity = limit_magnitude(self.velocity, self.max_speed)
        self.acceleration = np.zeros_like(self.acceleration)
        
    def edges(self) -> None:
        if self.position[0] > self.s_width:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = self.s_width
        if self.position[1] > self.s_heigh:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = self.s_heigh
            
    def toroidal_distance(self, pos1, pos2, width, height):
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        dx = min(dx, width - dx)
        dy = min(dy, height - dy)
        return np.sqrt(dx**2 + dy**2)
            
        
    def _align(self, boids:list['Boid']) -> np.ndarray:
        other_velocities = []
        for other in boids:
            distance = self.toroidal_distance(self.position, other.position, self.s_width, self.s_heigh)
            if self != other and distance < self.perception:
                other_velocities.append(other.velocity)
        
        if len(other_velocities) > 0:       
            steering_force = average_heading(np.array(other_velocities)) - self.velocity
            steering_force = limit_magnitude(steering_force, self.max_force)
            return steering_force
        else:
            return np.zeros_like(self.acceleration)   
        
    def _cohesion(self, boids:list['Boid']) -> np.ndarray:
        other_positions = []
        for other in boids:
            distance = self.toroidal_distance(self.position, other.position, self.s_width, self.s_heigh)
            if self != other and distance < self.perception:
                other_positions.append(other.position)
                
        if len(other_positions) > 0:
            steering_force = average_position(np.array(other_positions)) - self.position
            steering_force = steering_force - self.velocity
            steering_force = limit_magnitude(steering_force, self.max_force)
            return steering_force
        else:
            return np.zeros_like(self.velocity)
        
    def _separation(self, boids:list['Boid']) -> np.ndarray:
        new_vec = []
        for other in boids:
            distance = self.toroidal_distance(self.position, other.position, self.s_width, self.s_heigh)
            if self != other and distance < self.perception:
                tmp = self.position - other.position
                tmp = tmp / (distance + 1e-2)
                new_vec.append(tmp)
        if len(new_vec) > 0:
            steering_force = np.mean(np.array(new_vec), axis=0)
            steering_force = steering_force - self.velocity
            steering_force = limit_magnitude(steering_force, self.max_force)
            return steering_force
        else:
            return np.zeros_like(self.velocity)
                
                
    def flock(self, boids, align_mult, cohesion_mult, sep_mult) -> None:
        alignment = self._align(boids)
        cohesion = self._cohesion(boids)
        separation = self._separation(boids)
        
        alignment *= align_mult
        cohesion *= cohesion_mult
        separation *= sep_mult

        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation
    
    
    def show(self, screen):
        # pygame.draw.circle(surface, color, position, radius)
        color:tuple = (255, 255, 255)
        radius:float = 5
        pygame.draw.circle(
            screen,
            color,
            list(self.position),
            radius)


