from constants import PLAYER_SHOOT_SPEED, SHOT_RADIUS
import pygame
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y, player_direction):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = pygame.Vector2(0, 1).rotate(player_direction) * PLAYER_SHOOT_SPEED
        self.rect = pygame.Rect(x - SHOT_RADIUS, y - SHOT_RADIUS, SHOT_RADIUS * 2, SHOT_RADIUS * 2)

    def draw(self, surface):
        pygame.draw.circle(surface, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position