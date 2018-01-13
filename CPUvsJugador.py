import pygame
import time
import random

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

##########################################################################
##########################################################################
def sumdig(L):
    suma = 0
    for i in L: suma ^= i
    return suma
	
def sucesores(n):
	if n<1: return []
	if n==1: return [[0]]
	lista = []
	lista.append([n-2])
	if n>=3:
		lista.append([n-3])
		j = n-3
		for i in range(1,int((j/2))+1): lista.append([i,j-i])
	return lista

def mex(L):
	n=0
	while n in L: n += 1
	return n

listaG = [0,1]
listaG.extend([-1]*1000)
def gDawson(n):
	if listaG[n]!=-1:
		return listaG[n]
	listaMex = []
	for i in sucesores(n):
		if len(i)==1: listaMex.append(gDawson(i[0]))
		else: listaMex.append(gDawson(i[0])^gDawson(i[1]))
	mexx = mex(listaMex)
	listaG[n]=mexx
	return mexx

def sgDawson(L):
	suma = 0
	for i in L: suma ^= gDawson(i)
	return suma

def decabin(dec):
	bina = []
	while dec:
		bina.insert(0, dec & 1)
		dec >>= 1
	return bina
   
def apnim(posN, i=0):
    suma = sumdig(posN)
    if suma:
        bina, encontrado = len(decabin(suma)), False
        while not encontrado:
            sumando = decabin(posN[i])
            if len(sumando) < bina or sumando[-bina] == 0: i += 1
            else: encontrado = True
        return sumdig([suma,posN[i]]),i
    else: return
	
def calcMovDawson(L):
	#CASOS BASE
	if sgDawson(L) == 0:  return "Es P"
	if len(L)==1 and L[0]==1: return []
	result = L[:]
	valPilas = list(map(gDawson,L))
	gBuscado,indpilaCambiar = apnim(valPilas)
	pila = L[indpilaCambiar]
	if pila >= 2 and gDawson(pila-2)==gBuscado:
		result[indpilaCambiar]=pila-2
		result = [a for a in result if a != 0]
		return result
	for i in sucesores(pila):
		if len(i)==1 and sgDawson(i)==gBuscado:
			result[indpilaCambiar]=i[0]
			result = [a for a in result if a != 0]
			return result
		else:
			if sgDawson(i)==gBuscado:
				result[indpilaCambiar]=i[0]
				result.insert(indpilaCambiar+1,i[1])
				result = [a for a in result if a != 0]
				return result
##########################################################################
##########################################################################

def matrizPosToList(M):
	lista = []
	contador = 0
	for j in range(10):
		if M[0][j] == NEGRO and M[1][j] == VACIO and M[2][j] == BLANCO:
			contador = contador + 1
		else:
			if contador != 0:
				lista.append(contador)
			contador = 0
	if contador != 0:
		lista.append(contador)
	return lista

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

def hacerMovimientosObligatoriosN(M):
	listaColBlancoEnMedio = [j for j in range(10) if M[1][j]==BLANCO]
	for j in listaColBlancoEnMedio:
		if j-1>=0 and M[0][j-1]==NEGRO:
			M[0][j-1] = VACIO
			M[1][j] = NEGRO
			return True
		if j+1<=9 and M[0][j+1]==NEGRO:
			M[0][j+1] = VACIO
			M[1][j] = NEGRO
			return True
	return False

def hacerMovimientosObligatoriosB(M):
	listaColBlancoEnMedio = [j for j in range(10) if M[1][j]==NEGRO]
	for j in listaColBlancoEnMedio:
		if j-1>=0 and M[2][j-1]==BLANCO:
			M[2][j-1] = VACIO
			M[1][j] = BLANCO
			return True
		if j+1<=9 and M[2][j+1]==BLANCO:
			M[2][j+1] = VACIO
			M[1][j] = BLANCO
			return True
	return False

def hacerMovimientosObligatorios(M):
	while hacerMovimientosObligatoriosN(M):
		if not hacerMovimientosObligatoriosB(M): break
	
def moverIA():
	time.sleep(.4)
	if not hacerMovimientosObligatoriosB(matrizPos):
		listaBuscada = calcMovDawson(matrizPosToList(matrizPos))
		#print("Le paso a Dawson", matrizPosToList(matrizPos))
		movs = movimientosPosibles(matrizPos)
		random.shuffle(movs)
		for (j0,j) in movs:
			copiaMatrizPos = [a[:] for a in matrizPos]
			copiaMatrizPos[2][j0] = VACIO
			copiaMatrizPos[1][j] = BLANCO
			hacerMovimientosObligatorios(copiaMatrizPos)
			#print(listaBuscada, matrizPosToList(copiaMatrizPos))
			if listaBuscada == matrizPosToList(copiaMatrizPos):
				mover(2,j0,1,j)
				break

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
		if matrizPos[i][j] == NEGRO: screen.blit(peon_negro,(1+90*j,90*i))
		elif matrizPos[i][j] == BLANCO: screen.blit(peon_blanco,(1+90*j,90*i))
pygame.display.flip()

partidaTerminada = False
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: running = 0
		if turno == NEGRO and event.type == pygame.MOUSEBUTTONDOWN:
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
								turno = BLANCO
								if (i+j)%2==0:pygame.draw.rect(screen, marron_oscuro, matrizRect[i][j])
								else: pygame.draw.rect(screen, marron_claro, matrizRect[i][j])
								screen.blit(peon_negro,(1+90*nuevaCol,90))
								pygame.display.flip()
	
	if turno==BLANCO:
		moverIA()
		turno = NEGRO
		if not movimientosPosibles(matrizPos):
			partidaTerminada = True
			label = myfont.render("GANAN BLANCAS", 1, (255,255,0))
			screen.blit(label, (390, 273))
	#renderizado
	listaRectMov = listaRectMovPosibles()
	for i in range(3):
		for j in range(10):
			#recuadros
			if turno==NEGRO and (i,j) in listaRectMov: screen.blit(contorno_peon,(90*j,90*i))
			elif (i+j)%2==0:pygame.draw.rect(screen, marron_oscuro, matrizRect[i][j])
			else: pygame.draw.rect(screen, marron_claro, matrizRect[i][j])
			#peones
			if matrizPos[i][j] == NEGRO: screen.blit(peon_negro,(1+90*j,90*i))
			elif matrizPos[i][j] == BLANCO: screen.blit(peon_blanco,(1+90*j,90*i))
	pygame.display.flip()

quit()