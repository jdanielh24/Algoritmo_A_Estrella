import Nodo
import pygame
import Colores as C

def crearCuadricula(filas, ancho, mapa):
	cuadricula = []
	anchoCasilla = ancho // filas

	for i in range(filas):
		cuadricula.append([])
		for j in range(filas):
			nodo = Nodo.Nodo(i, j, anchoCasilla, filas)
			if (mapa[i][j] == 'P'):
				nodo.crearPasto()
			if (mapa[i][j] == 'B'):
				nodo.crearBosque()
			if (mapa[i][j] == 'M'):
				nodo.crearMontania()
			if (mapa[i][j] == 'A'):
				nodo.crearAgua()
			cuadricula[i].append(nodo)

	return cuadricula


def dibujarCuadricula(ventana, filas, ancho):
	anchoCasilla = ancho // filas
	for i in range(filas):
		pygame.draw.line(ventana, C.GRIS, (0, i * anchoCasilla), (ancho, i * anchoCasilla))
		for j in range(filas):
			pygame.draw.line(ventana, C.GRIS, (j * anchoCasilla, 0), (j * anchoCasilla, ancho))

def dibujar(ventana, cuadricula, filas, ancho):
	#ventana.fill(BLANCO)

	for fila in cuadricula:
		for nodo in fila:
			nodo.dibujar(ventana)

	dibujarCuadricula(ventana, filas, ancho)
	pygame.display.update()