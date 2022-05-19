"""
Archivo: mapa.py

	Este archivo contiene funcionesque pueden generar un mapa, en forma de matriz, con una distribución aleatoria de 
	los suelos (pasto, bosque, montaña o agua).

	Importaciones:
		> random: módulo utilizado para obtener números pseudoaleatorios.
"""

import random

def anadir_suelo_contiguo(mapa,  i, j, prob, tipo_suelo):
	"""
		Función recursiva, utilizada para añadir, con cierta probabilidad, el mismo tipo de suelo a los nodos vecinos 
		del nodo actual. La probabilidad va dismiyuendo en cada llamada a la función.

		Parámetros
   		----------
		mapa: list
			se almacena el valor del tipo de suelo para cada nodo. 
			Ejemplo:[	['P', 'P', 'B', 'P'], 
						['B', 'P', 'P', 'A'],  
						['P',''P', 'P', 'P'],
						['P',''M', 'M', 'P']
					]
		i: int
	   		fila en que se encuentra el nodo actual.
		j: int
			columna en donde se encuentra el nodo actual.
		prob: float
			probabilidad de que se añada el mismo tipo de suelo en los vecinos del nodo actual.
		tipo_suelo: str
			tipo de suelo: 'B', 'M' o 'A'
		
		Al terminar la función, un ejemplo de como quedaría mapa es el siguiente:
			[	['B', 'B', 'B', 'P'], 
				['B', 'B', 'P', 'A'],  
				['P',''B', 'M', 'A'],
				['P',''M', 'M', 'P']	
			]	
	"""
	
	if prob <= 0:
		return # terminar las llamadas recursivas cuando ya no exista probabilidad
	
	# si random.random() cae dentro de la probabilidad, se cambia el tipo de suelo del nodo mapa[i][j] al tipo de suelo en tipo_suelo
	if(random.random() < prob):
		mapa [i][j] = tipo_suelo
	
	if (i-1 >= 0 and j-1 >= 0) and (i+1 < len(mapa) and j+1 < len(mapa)): # validar que los vecinos se encuentren en los índices posibles
		# se mandará a llamar la función para cada nodo vecino
		# si no se disminuyera la probabilidad, la recursividad sería infinita
		# en cada nueva llamada, es menos probable que el suelo del nodo vecino sea el mismo que el del actual
		anadir_suelo_contiguo(mapa,  i-1,   j,      prob-0.1, tipo_suelo) # vecino de arriba
		anadir_suelo_contiguo(mapa,  i,     j-1,    prob-0.1, tipo_suelo) # vecino de la izquierda
		anadir_suelo_contiguo(mapa,  i,     j+1,    prob-0.1, tipo_suelo) # vecino de la derecha
		anadir_suelo_contiguo(mapa,  i+1,   j,      prob-0.1, tipo_suelo) # vecino de abajo


def anadirSuelos(mapa):
	"""
		Se añaden los tipos de suelos 'B', 'M' o 'A' en mapa, que originalmente solo contiene el tipo de suelo 'P'.
			'B' = Bosque (Mayor probabilidad).
			'M' = Montaña (Menor probabilidad que B pero mayor que A).
			'A' = Agua (Menor probabilidad).
			

		Parámetros
   		----------
		mapa: list
			se almacena el valor del tipo de suelo para cada nodo. 
			Ejemplo:[	['P', 'P', 'P', 'P'], 
						['P', 'P', 'P', 'P'],  
						['P',''P', 'P', 'P'],
						['P',''P', 'P', 'P']
					]
		

		Al terminar la función, un ejemplo de como quedaría mapa es el siguiente:
			[	['P', 'P', 'B', 'P'], 
				['B', 'P', 'P', 'A'],  
				['P',''P', 'P', 'P'],
				['P',''M', 'M', 'P']
			]
	"""
	
	SUELOS = ['B', 'M', 'A']
	PESOS = [0.5, 0.3, 0.2 ] # mientras mayor peso, mayor probabilidad tendrá. Son 3 pesos, correspondientes a los 3 tipos de suelos en SUELOS.
	
	for i in range(len(mapa)):
		for j in range(len(mapa[i])):
			if (random.random() > 0.97): # probabilidad baja, porque solo es True si random.random() es un número entre 1.0 y > 0.97
				suelo = random.choices(population=SUELOS, weights=PESOS, k=1)[0] # se selecciona un tipo de suelo de acuerdo al peso que cada uno tiene
				mapa[i][j] = suelo # mapa[i][j] tenía el valor 'P', pero ahora se será 'B', 'M' o 'A'
				anadir_suelo_contiguo(mapa, i, j, 0.5, suelo) # llamada para agregar el mismo tipo de suelo en los nodos vecinos.


def crear_mapa(filas):
	"""
		Función recursiva, utilizada para añadir, con cierta probabilidad, el mismo tipo de suelo a los nodos vecinos 
		del nodo actual. La probabilidad va dismiyuendo en cada llamada a la función.

		Parámetros
   		----------
		filas: int
	   		número de filas (y columnas) que debe de tener el mapa.	
	"""

	mapa = []
	for i in range(filas):
		mapa.append([]) # añadir una nueva list para cada i
		for j in range(filas):
			mapa[i].append('P') # se agrega 'P' a todas las casillas del mapa.
	
	anadirSuelos(mapa) # llamada para agregar los otros tipos de suelos.
	
	return mapa