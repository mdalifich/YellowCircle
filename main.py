import pygame
from random import randint

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Круг')
    size = width, height = 2000, 2000
    screen = pygame.display.set_mode(size)

    running = True
    x, y = 0, 0
    pps = 10# Pixels per Seconds. В учебнике v. 
    flag = False
    size = 0
    clock = pygame.time.Clock()
    screen.fill((0, 0, 250))
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    flag = True
                    screen.fill((0, 0, 250))
                    size = 0
        if flag:
            pygame.draw.circle(screen, (randint(0, 255), randint(0, 255), randint(0, 255)), (x, y), size)
            size += pps * clock.tick() / 1000
        pygame.display.flip()
    pygame.quit()