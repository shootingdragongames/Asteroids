import pygame #imports the open-source pygame
import random
import sys
from constants import *
from player import Player
from circleshape import CircleShape
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
def draw_menu(screen, title_small_font, title_large_font, menu_font, selected_option=0):
    screen.fill("black")
    studio_name = title_small_font.render("ShootingDragonGames'", True, "white")
    studio_rect = studio_name.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 - 60))
    screen.blit(studio_name, studio_rect)
    title = title_large_font.render("ASTEROIDS!", True, "white")
    title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
    screen.blit(title, title_rect)
    options =["PLAY", "LEVEL SELECT", "QUIT"]
    for i, option in enumerate(options):
        color = "yellow" if i == selected_option else "white"
        text = menu_font.render(option, True, color)
        text_rect = text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + i * 50))
        screen.blit(text, text_rect)
def menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    title_small_font = pygame.font.Font(None, 36)
    title_large_font = pygame.font.Font(None, 96)
    menu_font = pygame.font.Font(None, 64)
    clock = pygame.time.Clock()
    selected = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    selected = (selected - 1) % 3
                elif event.key == pygame.K_s:
                    selected = (selected + 1) % 3
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # PLAY
                        return True
                    elif selected == 1: # level select
                        print("Level select menu (comming soon [tm])")
                    else:  # QUIT
                        return False
        draw_menu(screen, title_small_font, title_large_font, menu_font, selected)
        pygame.display.flip()
        clock.tick(60)
def draw_level_select(screen, level_font, levels_unlocked, high_score, selected_level=0):
    screen.fill("black")
    title = level_font.render("SELECT LEVEL", True, "white")
    title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(title, title_rect)
    score_text = level_font.render(f"high score: {high_score}", True, "white")
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH /2, SCREEN_HEIGHT/4 + 50))
    screen.blit(score_text, score_rect)
    level_requirements = {}
    for level in range(1, 11):
        if level == 1:
            level_requirements[level] = 0
        else:
            level_requirements[level] = (level - 1) * 100
    for level in range(11, 21):
        level_requirements[level] = (level - 10) * 1000
    for level in range(21, 31):
        level_requirements[level] = level_requirements[20] + ((level - 20) * 10000)
    y_spacing = 40 #spacing between levels
    x_start = SCREEN_WIDTH / 4 # where the level select starts
    y_start = SCREEN_HEIGHT / 2 # starts lower than the title
    for level, required_score in level_requirements.items():
        is_unlocked = high_score >= required_score
        color = "white" if is_unlocked else "red"
        if level == selected_level and is_unlocked:
            color = "yellow"
        level_text = f"level {level}"
        if not is_unlocked:
            level_text += f" (REQUIRES {required_score} points)"
        text_surface = level_font.render(level_text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x = x_start
        text_rect.y = y_start + (level - 1) * y_spacing
        screen.blit(text_surface, text_rect)
def level_select(high_score):
    pass

def game():
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
def main():
    while True:
        play = menu()
        if play:
             game()
        else:
            break
    pygame.quit()
    
    

if __name__ == "__main__":
    main() #this ensures the main() function is only called when this file is imported as a module.
