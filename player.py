
from circleshape import CircleShape
from shot import Shot
import pygame
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOTCD, SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_INVINCIBLITY_TIME
class Player(CircleShape):
    shot_cd = 0
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        CircleShape.__init__(self, x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.last_hit_time = 0
        self.is_invincible = False
    # in the player class
    def can_be_hit(self):
        current_time = pygame.time.get_ticks() / 1000
        if self.is_invincible:
            if current_time - self.last_hit_time >= PLAYER_INVINCIBLITY_TIME:
                self.is_invincible = False
                return True
            return False
        return True
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    def draw(self, screen):
        current_time = pygame.time.get_ticks() / 1000
        if self.is_invincible and current_time -  self.last_hit_time < PLAYER_INVINCIBLITY_TIME:
            flash_rate = int(PLAYER_INVINCIBLITY_TIME * 200)
            if pygame.time.get_ticks() % flash_rate < (flash_rate // 2): #scaling flashing effect
                pygame.draw.polygon(screen, "white", self.triangle(), 2)
        else:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT

    def update(self, dt):
        if self.shot_cd > 0:
            self.shot_cd -= dt
        if self.shot_cd < 0:
            self.shot_cd = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
    def shoot(self):
        if self.shot_cd >0:
            return False
        x, y = self.position
        new_shot = Shot(x, y, self.rotation)
        self.shot_cd = PLAYER_SHOTCD
        return True

 


