import pygame
import time
from dawson import Dawson

pygame.init()
game = Dawson()
pygame.display.flip()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game.finished:
                game.reset()
            else:
                pos = pygame.mouse.get_pos()
                game.process_click(pos)
            game.draw_state()
            pygame.display.flip()

quit()
