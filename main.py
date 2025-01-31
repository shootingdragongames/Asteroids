import pygame #imports the open-source pygame
import random
import sys
from constants import *
from player import Player
from circleshape import CircleShape
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
def debug(screen, font, clock, debug=True):#set to false or delete this function before publishing
    if debug:
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 204, 0))
        screen.blit(fps_text, (10, 40))

def setup_screen(fullscreen = False):
    if fullscreen:
        display_info = pygame.display.Info()
        width = display_info.current_w
        height = display_info.current_h
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    else:
        width = 800
        height = 600
        screen = pygame.display.set_mode((width, height))
    return screen, width, height


def draw_menu(screen, title_small_font, title_large_font, menu_font, selected_option=0):
    screen.fill("black")
    actual_width = screen.get_width()
    actual_height = screen.get_height()
    studio_name = title_small_font.render("ShootingDragonGames'", True, "white")
    studio_rect = studio_name.get_rect(center=(actual_width * MENU_CENTER_X, actual_height * TITLE_HEIGHT))
    screen.blit(studio_name, studio_rect)
    title = title_large_font.render("ASTEROIDS!", True, "white")
    title_rect = title.get_rect(center=(actual_width * MENU_CENTER_X, actual_height * STUDIO_HEIGHT))
    screen.blit(title, title_rect)
    #menu options
    options = ["PLAY", "LEVEL SELECT", "QUIT"]
    for i, option in enumerate(options):
        color = "yellow" if i == selected_option else "white"
        text = menu_font.render(option, True, color)
        text_rect = title.get_rect( center=(actual_width * MENU_CENTER_X, actual_height * MENU_START_HEIGHT + i * MENU_SPACING))
        screen.blit(text, text_rect)
        
def menu():
    global FULLSCREEN
    pygame.init()
    screen, screen_width, screen_height = setup_screen(FULLSCREEN)
    title_small_font = pygame.font.Font(None, 36)
    title_large_font = pygame.font.Font(None, 96)
    menu_font = pygame.font.Font(None, 64)
    clock = pygame.time.Clock()
    selected = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, FULLSCREEN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f: #full screen button
                    FULLSCREEN =  not FULLSCREEN
                    screen, screen_width, screen_height = setup_screen(FULLSCREEN)
                if event.key == pygame.K_ESCAPE and FULLSCREEN:
                    FULLSCREEN = False
                    screen, screen_width, screen_height = setup_screen(FULLSCREEN)
                if event.key == pygame.K_w:
                    selected = (selected - 1) % 3
                elif event.key == pygame.K_s:
                    selected = (selected + 1) % 3
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # PLAY
                        return True, FULLSCREEN
                    elif selected == 1: # level select
                        print("Level select menu (comming soon [tm])")
                    else:  # QUIT
                        return False
        draw_menu(screen, title_small_font, title_large_font, menu_font, selected)
        pygame.display.flip()
        clock.tick(60)

def draw_level_select(screen, level_font, levels_unlocked, high_score, selected_level=0):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    screen.fill("black")
    title = level_font.render("SELECT LEVEL", True, "white")
    title_rect = title.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(title, title_rect)
    score_text = level_font.render(f"high score: {high_score}", True, "white")
    score_rect = score_text.get_rect(center=(screen_width / 2, screen_height / 4 + 50))
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
    x_start = screen_width / 4 # where the level select starts
    y_start = screen_height / 2 # starts lower than the title
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

def game(fullscreen=False):
    global FULLSCREEN
    FULLSCREEN = fullscreen
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
    screen, screen_width, screen_height = setup_screen(fullscreen)
    asteroid_field = AsteroidField(screen.get_width(), screen.get_height())
    player = Player(screen_width / 2, screen_height / 2, screen_width, screen_height)
    print("Starting asteroids!") #prints to the screen the next few lines
    print(f"Screen width: {screen_width}")
    print(f"Screen height: {screen_height}")
    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return #these three lines are needed to make the x button work on the window, otherwise you have to hit ctrl+c to exit the program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    FULLSCREEN = not FULLSCREEN
                    o_width = screen_width
                    o_height = screen_height
                    screen, screen_width, screen_height = setup_screen(FULLSCREEN)
                    width_scale = screen_width / o_width
                    height_scale = screen_height / o_height
                    for sprite in drawable:
                        sprite.position.x = int(sprite.position.x * width_scale)
                        sprite.position.y = int(sprite.position.y * height_scale)
                    player.position.x = int(player.position.x * width_scale)
                    player.position.y = int(player.position.y * height_scale)
                    for shot in shots:
                        shot.position.x = int(shot.postion.x * width_scale)
                        shot.position.y = int(shot.position.y * height_scale)
                if event.key == pygame.K_ESCAPE and FULLSCREEN:
                    FULLSCREEN = False
                    o_width = screen_width
                    o_height = screen_height
                    screen, screen_width, screen_height = setup_screen(FULLSCREEN)
                    width_scale = screen_width / o_width
                    height_scale = screen_height / o_height
                    for sprite in drawable:
                        sprite.position.x = int(sprite.position.x * width_scale)
                        sprite.position.y = int(sprite.position.y * height_scale)
                    player.position.x = int(player.position.x * width_scale)
                    player.position.y = int(player.position.y * height_scale)
                    for shot in shots:
                        shot.position.x = int(shot.position.x * width_scale)
                        shot.position.y = int(shot.positon.y * height_scale)

        screen.fill("black") #fills the screen with a string color
        debug(screen, font, clock)
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
            text_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 2))
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
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))
        pygame.display.flip() #updates the screen
def main():
    while True:
        play, fullscreen = menu()
        if play:
             game(fullscreen)
        else:
            break
    pygame.quit()
    
    

if __name__ == "__main__":
    main() #this ensures the main() function is only called when this file is imported as a module.
