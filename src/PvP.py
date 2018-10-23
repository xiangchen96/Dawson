import pygame
import time
import dawson

pygame.init()

WIDTH = 10
screen = pygame.display.set_mode((90*WIDTH, 300))

myfont = pygame.font.SysFont("monospace", 20)
running = True
turn = dawson.WHITE

matrizPos = [[0]*WIDTH for _ in range(3)]
matrizRect = [["PLACEHOLDER"]*WIDTH for _ in range(3)]

dawson.reset(matrizPos)

# draw board
for i in range(3):
    for j in range(WIDTH):
        matrizRect[i][j] = pygame.Rect((90*j), (90*i), 90, 90)
        if (i+j) % 2 == 0:
            pygame.draw.rect(screen, dawson.dark_brown, matrizRect[i][j])
        else:
            pygame.draw.rect(screen, dawson.clear_brown, matrizRect[i][j])

game_finished = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_finished:
                dawson.reset(matrizPos)
                turn = dawson.WHITE
                game_finished = False
                # hide winner
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 270, 900, 30))
            else:
                pos = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(WIDTH):
                        if matrizRect[i][j].collidepoint(pos) and matrizPos[i][j] == turn:
                            movs = dawson.possible_moves(matrizPos, turn)
                            if j in [x for (x, _) in movs]:
                                aux = 0
                                for (a, b) in movs:
                                    if a == j:
                                        break
                                    else:
                                        aux += 1
                                col, new_col = movs[aux]
                                dawson.move(matrizPos, i, j, 1, new_col)
                                turn = dawson.pass_turn(turn)
                                if not dawson.possible_moves(matrizPos, turn):
                                    game_finished = True
                                    winner = "BLACK" if turn == dawson.WHITE else "WHITE"
                                    label = myfont.render(winner+" WINS", 1, (255, 255, 0))
                                    screen.blit(label, (390, 273))
    moves_rect = dawson.rect_possible_moves(matrizPos, turn)
    dawson.draw_state(screen, matrizPos, matrizRect, moves_rect)
    pygame.display.flip()

quit()
