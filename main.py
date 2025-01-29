import pygame #imports the open-source pygame
import random
import sys
from constants import *
from player import Player
from circleshape import CircleShape
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
def main():
    pygame.init() #starts pygame
    score = 0
    font = pygame.font.Font(None, 36)
    game_over = False
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group() 
    shots = pygame.sprite.Group()
    Shot.containers = shots
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Player.containers = (updatable, drawable)
    asteroid_field = AsteroidField()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # starts a game window with pygame with the varibles set in constrants.py
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    print("Starting asteroids!") #prints to the screen the next few lines
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return #these three lines are needed to make the x button work on the window, otherwise you have to hit ctrl+c to exit the program
        screen.fill("black") #fills the screen with a string color
        clock.tick(60)
        for asteroid in asteroids:
            if asteroid.crossed(player) and player.can_be_hit():
                if not game_over:
                    score -= 10
                    player.last_hit_time = pygame.time.get_ticks() / 1000
                    player.is_invincible = True
                    if score < 0:
                        game_over = True
                    
        if game_over:
            game_over_text = font.render("GAME OVER", True, "red")
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(game_over_text, text_rect)
        else:
            shots.update(dt)
            player.update(dt)
            updatable.update(dt)

        for sprite in drawable:
            sprite.draw(screen)
        player.draw(screen)
        for shot in shots:
            shot.draw(screen)
        for asteroid in asteroids:
            for shot in shots:
                if pygame.sprite.collide_rect(asteroid, shot):
                    score += 10
                    asteroid.split()
                    shot.kill()
        
        for obj in drawable:
            obj.draw(screen)
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))
        pygame.display.flip() #updates the screen
    
    
    

if __name__ == "__main__":
    main() #this ensures the main() function is only called when this file is imported as a module.
