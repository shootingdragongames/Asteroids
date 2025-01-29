import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS



class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        pygame.sprite.Sprite.__init__(self, self.containers)
        super().__init__(x, y, radius)
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
    def draw(self, surface):
        pygame.draw.circle(surface, "white", self.position, self.radius, 2)
    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
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
        
