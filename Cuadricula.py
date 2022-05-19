"""
Archivo: cuadricula.py

	Contiene funciones para crear y dibujar el mapa como una cuadrícula, en la que cada casilla será un objeto Nodo. 
	También tiene un método para construir el camino final.

	Importacioness:
		> Nodo: módulo que provee objetos del tipo Nodo, para almacenar todo su información (tipo, color, costos, posición, etc).
		> pygame: módulo que permite la creación de videojuegos en dos dimensiones.
		> colores: módulo que provee un conjunto de diferentes colores en formato RGB.
"""

from nodo import Nodo
import pygame
import colores as Color

def crearCuadricula(filas, ancho, mapa):
	"""
		Crea un objeto list que representa la cuadrícula, la cuál está conformada por casillas, donde cada una es un Nodo.

		Parámetros
   		----------
		filas: int
	   		número de filas (y columnas) que debe de tener la cuadricula.
		ancho: int
	   		ancho (y alto) de toda la cuadrícula (# de pixeles).
		mapa: list
	   		contiene la distribución de los suelos en el mapa.		   	
	"""	

	cuadricula = []
	anchoCasilla = ancho // filas # obtener la medida de cada casilla

	for i in range(filas):
		cuadricula.append([])
		for j in range(filas):
			nodo = Nodo(i, j, anchoCasilla, filas) # crear Nodo para el objeto cuadricula[i][j]
			
			# dependiendo del tipo de suelo que se encuentre en mapa[i][j] se le asignará al nodo actual
			if (mapa[i][j] == 'P'):
				nodo.crearPasto()
			if (mapa[i][j] == 'B'):
				nodo.crearBosque()
			if (mapa[i][j] == 'M'):
				nodo.crearMontania()
			if (mapa[i][j] == 'A'):
				nodo.crearAgua()
			cuadricula[i].append(nodo) # agregar el nodo en cuadricula

	return cuadricula


def dibujarCuadricula(ventana, filas, ancho):
	"""
		Se dibujan las rayas verticales y horizontales en la ventana, las cuales sirven para hacer las divisiones entre casillas.

		Parámetros
   		----------
		ventana: pygame.Surface
	   		objeto que representa la ventana para la partida.
		filas: int
	   		número de filas (y columnas) que debe de tener la cuadricula.
		ancho: int
	   		ancho (y alto) de toda la cuadrícula (# de pixeles).
	"""
	anchoCasilla = ancho // filas
	
	for i in range(filas):
		pygame.draw.line(ventana, Color.GRIS, (0, i * anchoCasilla), (ancho, i * anchoCasilla)) # rayas horizontales
		for j in range(filas):
			pygame.draw.line(ventana, Color.GRIS, (j * anchoCasilla, 0), (j * anchoCasilla, ancho)) # rayas verticales

def dibujar(ventana, cuadricula, filas, ancho):
	"""
		Se dibuja la cuadricula en la ventana.
		La cuadricula ya contiene los nodos con su respectiva información (ej: el tipo de suelo)

		Parámetros
   		----------
		ventana: pygame.Surface
	   		objeto que representa la ventana para la partida.
		cuadricula: list
			contiene todos los nodos que conforman la cuadricula.
		filas: int
	   		número de filas (y columnas) que debe de tener la cuadricula.
		ancho: int
	   		ancho (y alto) de toda la cuadrícula (# de pixeles).	
	"""
	for fila in cuadricula:
		for nodo in fila:
			nodo.dibujar(ventana) # se dibuja el nodo en cuestión (cambia el tipo de color, el margen, el costo mostrado, etc)

	dibujarCuadricula(ventana, filas, ancho)
	pygame.display.update()


def reconstruirCamino(provieneDe, actual, dibujar):
	"""
		Reconstruye el camino entre el nodo de inicio y el del fin.

		Parámetros
   		----------
		provieneDe: Nodo
	   		Nodo padre
		actual: Nodo
	   		nodo actual	
		dibujar: function
	   		función para dibujar la cuadricula en la ventana.
	"""
	actual.crearCamino() # en este punto, actual corresponde al nodo final (objetivo)
	
	# se recorre la ruta para crear el camino final, viendo cuál es el nodo padre del nodo actual.
	while actual in provieneDe:
		actual = provieneDe[actual]
		actual.crearCamino()
		dibujar()
