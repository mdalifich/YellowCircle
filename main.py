import pygame
from random import randint
import Cube
from Cube import *

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Куб')
    size = width, height = 150, 150
    screen = pygame.display.set_mode(size)
    cube = Cubic(0, 0, screen)
    running = True
    while running:
        screen.fill((0, 0, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        cube.draw()
        pygame.display.flip()
    pygame.quit()