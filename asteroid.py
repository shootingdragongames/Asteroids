import pygame
import random
import math
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_POINTS



class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        pygame.sprite.Sprite.__init__(self, self.containers)
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.random_offset = [random.random() for _ in range(ASTEROID_POINTS)]

    def draw(self, surface):
        #changed from pygame.draw.circle to pygame.draw.polygon
        points = []
        for i in range(ASTEROID_POINTS):
            angle = (2 * math.pi * i) / ASTEROID_POINTS
            radius = self.radius * (0.8 + 0.4 * self.random_offset[i])
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(surface, "white", points, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.x = self.position.x
        self.y = self.position.y
        self.rect.center = (self.x, self.y)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        randomangle = random.uniform(20, 50)
        newvel1 = self.velocity.rotate(randomangle)
        newvel2 = self.velocity.rotate(-randomangle)
        newradius = self.radius - ASTEROID_MIN_RADIUS
        aster1 = Asteroid(self.position.x, self.position.y, newradius)
        aster2 = Asteroid(self.position.x, self.position.y, newradius)
        aster1.velocity = newvel1 * 1.2
        aster2.velocity = newvel2 * 1.2

