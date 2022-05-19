"""
Archivo: a_estrella.py

	Contiene las funciones para utilizar el algoritmo de búsqueda A*.

	Importaciones:
		> pygame: módulo que permite la creación de videojuegos en dos dimensiones.
		> PriorityQueue: Estructura de datos, donde cada valor en la cola tiene cierta prioridad.
		> cuadricula: módulo crear y dibujar el mapa como una cuadrícula, en la que cada casilla será un objeto Nodo. 
"""

import pygame
from queue import PriorityQueue
import cuadricula as Cuadricula

def h(p1, p2):
	"""
		Función para calcular la heurística.

		Parámetros
   		----------
		p1: tuple
	   		punto de partida (x, y).
		p2: tuple
	   		punto objetivo (x, y).   	
	"""	
	x1, y1 = p1
	x2, y2 = p2
	
	return abs(x1 - x2) + abs(y1 - y2) # obtener valores absolutos para las distancias en los ejes X y Y


def algoritmo(dibujar, cuadricula, inicio, fin):
	"""
		Algoritmo de búsqueda A*, el cuál calcula el camino más corto entre dos nodos, según la distancia entre estos
		y el costo para moverse entre nodos.

		Parámetros
   		----------
		dibujar: function
	   		función para dibujar la cuadricula en la ventana
		cuadricula: list
			contiene todos los nodos que conforman la cuadricula
		inicio: Nodo
	   		Nodo de inicio
		fin: Nodo
	   		nodo de fin (objetivo)
	"""
	contador = 0 # se utiliza para ver qué nodo se almacenó primero en listaAbierta si existe un empate de prioridades
	listaAbierta = PriorityQueue()
	listaAbierta.put((0, contador, inicio))  # cada elemento de listaAbierta será una tupla (x, y, z) donde x = f, y = contador, z = nodo
	provieneDe = {} # se guardará la relación entre los nodos y sus padres
	g = {nodo: float("inf") for fila in cuadricula for nodo in fila} # se asigna el valor infinito de g a cada nodo, para representar que se desconoce hasta el momento 
	g[inicio] = 0
	f = {nodo: float("inf") for fila in cuadricula for nodo in fila} # se asigna el valor infinito de f a cada nodo, para representar que se desconoce hasta el momento
	f[inicio] = h(inicio.getPosicion(), fin.getPosicion()) # se calcula f para el nodo de inicio
	inicio.setF(f[inicio]) 

	listaAbiertaHash = {inicio} # guardará los mismos valores que listaAbierta, pero dado que esta es un dict, será útil para verificar si contiene a un nodo en específico, porque PriorityQueue no nos otorga esa posibilidad

	while not listaAbierta.empty(): # repetir pasos hasta que no exista elementos en listaAbierta
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				pygame.quit()

		actual = listaAbierta.get()[2] # obtiene el elemento con más prioridad. En el indice [2] se encuentra el nodo.
		listaAbiertaHash.remove(actual) # también se remueve de listaAbiertaHash para manterla actualizada

		if actual == fin:
			# si el nodo actual es el mismo que el fin, entonces se ha encontrado el objetivo con la ruta más costa
			Cuadricula.reconstruirCamino(provieneDe, fin, dibujar) # constuir camino final
			return True

		# recorrer los vecinos del nodo actual
		for vecino in actual.vecinos:
			g_temporal = g[actual] + vecino.getCosto() # g hasta el momento + el costo que nos cuesta movernos al nodo vecino
			
			if g_temporal < g[vecino]:	
				provieneDe[vecino] = actual # indicar el nodo actual como padre del nodo vecino
				g[vecino] = g_temporal # indicar g del nodo vecino
				f[vecino] = g_temporal + h(vecino.getPosicion(), fin.getPosicion()) # calcular f del nodo vecino
				
				vecino.setF(f[vecino]) 
				
				if vecino not in listaAbiertaHash:
					# si el vecino a un no se encuentra en la lista abierta, guardarlo ahí
					contador += 1
					listaAbierta.put((f[vecino], contador, vecino))
					listaAbiertaHash.add(vecino)
					vecino.crearAbierto() # marco rojo,  este nodo lo pusimos en la lista abierta
					
		dibujar()

		if actual != inicio:
			actual.crearCerrado() # marco azul, ya no cambiará ningún valor
		
	return False 