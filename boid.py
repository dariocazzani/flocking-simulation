"""
Boids Simulation Module
=======================

Author: Dario Cazzani
Date: 2023-07-04

This module contains the Boid class and related utility functions for simulating
flocking behavior using the Boids algorithm inspired by Craig Reynolds' work:
https://www.red3d.com/cwr/boids/

Please refer to the LICENSE file for licensing information.
"""

import pygame
import numpy as np
import random


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
        self.velocity = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
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
            
    def _calculate_steering_forces(self, boids:list['Boid']) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        other_velocities = []
        other_positions = []
        separation_vectors = []
        min_separation_distance = float('inf')
        
        for other in boids:
            distance = self.toroidal_distance(self.position, other.position, self.s_width, self.s_heigh)
            if self != other and distance < self.perception:
                # for alignment
                other_velocities.append(other.velocity)
                # for cohesion
                other_positions.append(other.position)
                # for separation
                tmp = self.position - other.position
                tmp = tmp / (distance + 1e-2)
                separation_vectors.append(tmp)
                
                # Keep track of the minimum separation distance
                min_separation_distance = min(min_separation_distance, distance)
                    
        # alignment steering force
        if len(other_velocities) > 0:
            align_steering_force = average_heading(np.array(other_velocities)) - self.velocity
            align_steering_force = limit_magnitude(align_steering_force, self.max_force)
        else:
            align_steering_force = np.zeros_like(self.acceleration)

        # cohesion steering force
        if len(other_positions) > 0:
            cohesion_steering_force = average_position(np.array(other_positions)) - self.position
            cohesion_steering_force = cohesion_steering_force - self.velocity
            cohesion_steering_force = limit_magnitude(cohesion_steering_force, self.max_force)
        else:
            cohesion_steering_force = np.zeros_like(self.velocity)

        # separation steering force
        if len(separation_vectors) > 0:
            separation_steering_force = np.mean(np.array(separation_vectors), axis=0)
            separation_steering_force = separation_steering_force - self.velocity

            # Apply stronger force when boids are too close.
            min_distance_for_strong_separation = 25.0
            if min_separation_distance < min_distance_for_strong_separation:
                max_force = self.max_force * 2
            else:
                max_force = self.max_force

            separation_steering_force = limit_magnitude(separation_steering_force, max_force)
        else:
            separation_steering_force = np.zeros_like(self.velocity)
            
        return align_steering_force, cohesion_steering_force, separation_steering_force

                    
                
    def calculate_new_state(self, boids, align_mult, cohesion_mult, sep_mult):
        align_force, cohesion_force, separation_force = self._calculate_steering_forces(boids)

        align_force *= align_mult
        cohesion_force *= cohesion_mult
        separation_force *= sep_mult
        
        new_acceleration = self.acceleration + align_force + cohesion_force + separation_force
        new_velocity = self.velocity + new_acceleration
        new_position = self.position + new_velocity
        
        return new_position, new_velocity, new_acceleration
    
    
    def apply_new_state(self, new_state):
        new_position, new_velocity, new_acceleration = new_state
        self.position = new_position
        self.velocity = new_velocity
        self.acceleration = new_acceleration
        noise = np.random.normal(0, 0.1, 2)
        self.acceleration += noise
        self.update()
    
    
    def show(self, screen, size:float):
        angle = np.arctan2(self.velocity[1], self.velocity[0])

        point1 = np.array([np.cos(angle), np.sin(angle)]) * size + self.position
        point2 = np.array([np.cos(angle + 2.3), np.sin(angle + 2.3)]) * size/2 + self.position
        point3 = np.array([np.cos(angle - 2.3), np.sin(angle - 2.3)]) * size/2 + self.position
        
        p1 = [int(point1[0]), int(point1[1])]
        p2 = [int(point2[0]), int(point2[1])]
        p3 = [int(point3[0]), int(point3[1])]
        color = (255, 255, 255)

        pygame.draw.polygon(screen, color, [p1, p2, p3])
