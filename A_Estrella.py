import pygame
from queue import PriorityQueue
import Cuadricula

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p
	return abs(x1 - x2) + abs(y1 - y2)


def algoritmo(dibujar, cuadricula, inicio, fin):
	contador = 0
	listaAbierta = PriorityQueue()
	listaAbierta.put((0, contador, inicio))
	provieneDe = {}
	g = {nodo: float("inf") for fila in cuadricula for nodo in fila}
	g[inicio] = 0
	f = {nodo: float("inf") for fila in cuadricula for nodo in fila}
	f[inicio] = h(inicio.getPosicion(), fin.getPosicion())

	listaAbiertaHash = {inicio}

	while not listaAbierta.empty():
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				pygame.quit()

		actual = listaAbierta.get()[2]
		listaAbiertaHash.remove(actual)

		if actual == fin:
			Cuadricula.reconstruirCamino(provieneDe, fin, dibujar)
			fin.crearFinal()
			return True

		for vecino in actual.vecinos:
			g_temporal = g[actual] + vecino.getCosto()
			if g_temporal < g[vecino]:
				
				provieneDe[vecino] = actual
				g[vecino] = g_temporal
				f[vecino] = g_temporal + h(vecino.getPosicion(), fin.getPosicion())
				
				actual.setF(f[actual])
				vecino.setF(f[vecino])
				
				if vecino not in listaAbiertaHash:
					contador += 1
					listaAbierta.put((f[vecino], contador, vecino))
					listaAbiertaHash.add(vecino)
					vecino.crearAbierto()	
					
		dibujar()

		if actual != inicio:
			actual.crearCerrado()
		
	return False 