import pygame
import time

"""
DAWSON
quitar 1 si la pila es completa -> mover ultimo
quitar 2 -> mover ultimo con vecino
quitar 3 y no dividir -> mover penultimo
quitar 3 y dividir -> mover otra
"""

pygame.init()
screen = pygame.display.set_mode((900, 300))

myfont = pygame.font.SysFont("monospace", 20)
marron_oscuro=102,51,0
marron_claro=166,127,88
running, BLANCO = 1, 1
NEGRO, VACIO = -1, 0
turno = BLANCO

matrizPos = [[0 for i in range(10)] for i in range(3)]
matrizRect = [["PLACEHOLDER" for i in range(10)] for i in range(3)]
peon_negro = pygame.image.load("./images/bpawn.png")
peon_blanco = pygame.image.load("./images/wpawn.png")
contorno_peon = pygame.image.load("./images/borde.png")

def movimientosPosibles(M):
	#devuelve lista con (columnaIni,columnaDest)
	movs = []
	if turno == BLANCO:
		listaColNegraEnMedio = [j for j in range(10) if M[1][j]==NEGRO]
		for j in listaColNegraEnMedio:
			if j-1>=0 and M[2][j-1]==BLANCO: movs.append((j-1,j))
			if j+1<=9 and M[2][j+1]==BLANCO: movs.append((j+1,j))
		#no hay obligatorios
		if not movs:
			for j in range(10):
				if M[2][j]==BLANCO and M[1][j]==VACIO: movs.append((j,j))
	else:
		listaColBlancoEnMedio = [j for j in range(10) if M[1][j]==BLANCO]
		for j in listaColBlancoEnMedio:
			if j-1>=0 and M[0][j-1]==NEGRO: movs.append((j-1,j))
			if j+1<=9 and M[0][j+1]==NEGRO: movs.append((j+1,j))
		#no hay obligatorios
		if not movs:
			for j in range(10):
				if M[0][j]==NEGRO and  M[1][j]==VACIO: movs.append((j,j))
	return movs

def mover(i0,j0,i,j):
	color = matrizPos[i0][j0]
	matrizPos[i0][j0] = VACIO
	matrizPos[i][j] = color

def listaRectMovPosibles():
	movs = movimientosPosibles(matrizPos)
	lista = []
	if turno == BLANCO:
		for j in [x for (x,_) in movs]:
			lista.append((2,j))
	else:
		for j in [x for (x,_) in movs]:
			lista.append((0,j))
	return lista
	
def reset():
	for i in range(3):
		for j in range(10):
			if i == 0:
				matrizPos[i][j]=NEGRO
			elif i == 2:
				matrizPos[i][j]=BLANCO
			else:
				matrizPos[i][j]=VACIO

reset()
#pinto tablero y fichas iniciales
for i in range(3):
	for j in range(10):
		matrizRect[i][j] = pygame.Rect((90*j), (90*i), 90, 90)
		if (i+j)%2==0: pygame.draw.rect(screen, marron_oscuro, matrizRect[i][j])
		else: pygame.draw.rect(screen, marron_claro, matrizRect[i][j])

partidaTerminada = False

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: running = 0
		if event.type == pygame.MOUSEBUTTONDOWN:
			if partidaTerminada:
				reset()
				turno = BLANCO
				partidaTerminada = False
				#tapo "GANAN BLANCAS"
				pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 270, 900, 30))
			else:
				pos = pygame.mouse.get_pos()
				for i in range(3):
					for j in range(10):
						if matrizRect[i][j].collidepoint(pos) and matrizPos[i][j]==turno:
							movs = movimientosPosibles(matrizPos)
							if j in [x for (x,_) in movs]:
								aux = 0
								for (a,b) in movs:
									if a == j: break
									else: aux += 1
								col,nuevaCol = movs[aux]
								mover(i,j,1,nuevaCol)
								if turno==BLANCO:
									turno = NEGRO
									if not movimientosPosibles(matrizPos):
										partidaTerminada = True
										label = myfont.render("GANAN BLANCAS", 1, (255,255,0))
										screen.blit(label, (390, 273))
								else:
									turno = BLANCO
									if not movimientosPosibles(matrizPos):
										partidaTerminada = True
										label = myfont.render("GANAN NEGRAS", 1, (255,255,0))
										screen.blit(label, (390, 273))
	listaRectMov = listaRectMovPosibles()
	for i in range(3):
		for j in range(10):
			#recuadros
			if (i,j) in listaRectMov: screen.blit(contorno_peon,(90*j,90*i))
			elif (i+j)%2==0:pygame.draw.rect(screen, marron_oscuro, matrizRect[i][j])
			else: pygame.draw.rect(screen, marron_claro, matrizRect[i][j])
			#peones
			if matrizPos[i][j] == NEGRO: screen.blit(peon_negro,(1+90*j,90*i))
			elif matrizPos[i][j] == BLANCO: screen.blit(peon_blanco,(1+90*j,90*i))
	pygame.display.flip()

quit()