import pygame #imports the open-source pygame
from constants import *
def main():
    pygame.init #starts pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # starts a game window with pygame with the varibles set in constrants.py    
    print("Starting asteroids!") #prints to the screen the next few lines
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black") #fills the screen with a string color
        pygame.display.flip() #updates the screen
    
    
    

if __name__ == "__main__":
    main() #this ensures the main() function is only called when this file is imported as a module.
