"""
Archivo: juego.py

	Este archivo contiene la lógica de programación para ejecutar partidas utilizando el algoritmo A-estrella.
	Crea una ventana donde se creará un mapa, una cuadrícula y se podrán seleccionar los nodos de inicio, final 
	y obstáculos.

	Importaciones:
		> pygame: módulo que permite la creación de videojuegos en dos dimensiones.
		> tkinter: módulo que provee un conjunto de herramientas GUI.
		> mapa: módulo que se encarga de generar un mapa, en forma de matriz, con una distribución aleatoria de 
		los suelos (pasto, bosque, montaña o agua).
		> cuadricula: módulo para crear la cuadrícula que contendrá toda la información de los nodos, además de 
		que contiene métodos para dibujar y construir los caminos.
		> a_estrella: módulo que contiene el algoritmo de búsqueda A*.
"""

import pygame
from tkinter import *
from tkinter import messagebox
import mapa
import cuadricula 
import a_estrella

class Juego:
	"""
		Clase utilizada para crear una partida.

		Atributos
    	----------
    	DIMENSIONES_POSIBLES : list
        	contiene el número de casillas por filas y columnas que una partida puede tener.
			El mapa más pequeño puede ser de 4x4 y el más grande de 50x50.
    	indice_dim : int
        	indice para saber cuál valor de DIMENSIONES_POSIBLES se está utilizando.
	"""

	DIMENSIONES_POSIBLES = [4, 6, 8, 10, 16, 20, 25, 32, 40, 50]
	indice_dim = 9


	def __init__(self, ventana, ancho):
		"""
			Inicializar la ventana para las partidas.

			Parámetros
    		----------
			ventana: game.Surface
        		objeto que representa la ventana para la partida.
			ancho: int
				resolución, en pixeles, que tendrá la ventana.			
		"""

		self.ventana = ventana
		self.ancho = ancho
		

	def ejecutar(self):
		"""
			Este método contiene la lógica y control de las partidas.
		"""
		
		filas = self.DIMENSIONES_POSIBLES[self.indice_dim] #filas puede ser 4, 6, ... , 40 o 50.
		
		mapa_actual = mapa.crear_mapa(filas) # mapa_actual es un objeto list que contiene la distribución de los suelos en el mapa
		cuadricula_actual = cuadricula.crearCuadricula(filas, self.ancho, mapa_actual) # cuadricula_actual es un objeto list con los nodos del mapa ya creados.

		# nodos de inicio (punto de partida) y final (objetivo)
		inicio = None
		fin = None

		run = True # para controlar cuándo se detiene la partida

		Tk().wm_withdraw() # para ocultar la ventana principal que genera Tk
		messagebox.showinfo('¡Importante!', 'Asegurate de hacer click en la ventana del juego.\nPresiona la tecla [h] si deseas ver los controles.') # mensaje de advertencia
		
		while run:
			pygame.display.set_caption("Proyecto IA algoritmo estrella. Tablero de " + str(self.DIMENSIONES_POSIBLES[self.indice_dim]) + "x" + str(self.DIMENSIONES_POSIBLES[self.indice_dim]) + " casillas" ) # establecer título de la ventana. Ejemplo: Proyecto IA ... Tablero de 32x32 casillas

			cuadricula.dibujar(self.ventana, cuadricula_actual, filas, self.ancho) # dibujar la cuadricula, ya con el mapa generado, en la ventana
			
			# manejo de eventos (acciones con mouse o teclado):
			for evento in pygame.event.get():
				if evento.type == pygame.QUIT:
					# terminar la partida
					run = False

				if pygame.mouse.get_pressed()[0]: # click izquierdo
					posicion = pygame.mouse.get_pos() # posicion => (x, y)
					fila, columna = self.obtenerPosicionDeClick(posicion, filas, self.ancho) # obtener la fila y columna de la casilla donde se hizo click
					nodo = cuadricula_actual[fila][columna] # nodo seleccionado

					if not inicio and nodo != fin:
						# si no se ha puesto el nodo de inicio y el nodo seleccionado no es el final, crear el nodo de inicio
						inicio = nodo
						inicio.crearInicio()

					elif not fin and nodo != inicio:
						# si no se ha puesto el nodo de fin y el nodo seleccionado no es el inicio, crear el nodo final
						fin = nodo
						fin.crearFinal()

					elif nodo != fin and nodo != inicio:
						# si el nodo seleccionado no es el inicio ni el fin, crear un nodo barrera
						nodo.crearBarrera()

				elif pygame.mouse.get_pressed()[2]: # click derecho
					posicion = pygame.mouse.get_pos() # posicion => (x, y)
					fila, columna = self.obtenerPosicionDeClick(posicion, filas, self.ancho) # obtener la fila y columna de la casilla donde se hizo click
					nodo = cuadricula_actual[fila][columna]  # nodo seleccionado
					
					# se resetea el nodo seleccionado, cualquiera que sea su tipo (pasto, bosque, montaña, agua, inicio, fin o obstáculo) se pondrá como nodo de pasto.
					nodo.reiniciar()
					
					if nodo == inicio:
						inicio = None # si era de inicio, indicar que ya no existe un nodo de inicio
					elif nodo == fin:
						fin = None # si era de fin, indicar que ya no existe un nodo de fin

				if evento.type == pygame.KEYDOWN:
					if evento.key == pygame.K_SPACE and inicio and fin:
						# si se presiona la tecla de [espacio] y hay nodos de inicio y fin, comenzar a buscar el camino

						# recorrer los nodos de cuadricula_actual
						for fila in cuadricula_actual:
							for nodo in fila:
								nodo.actualizarVecinos(cuadricula_actual) # indicar cuáles son los nodos de cada vecino (por si existen barreras)
					
						Tk().wm_withdraw() # para ocultar la ventana principal que genera Tk

						# a_estrella.algoritmo() devuelve True si se encuentra un camino, de lo contrario False.
						if a_estrella.algoritmo(lambda: cuadricula.dibujar(self.ventana, cuadricula_actual, filas, self.ancho), cuadricula_actual, inicio, fin):
							messagebox.showinfo('Éxito','¡Camino encontrado con éxito!\nCosto total: ' + str(fin.getF()) )
						else:
							messagebox.showinfo('Error','No existe solución')
				
					if evento.key == pygame.K_h:
						# si se presiona la tecla [h], se muestra un cuadro ayuda
						Tk().wm_withdraw() # para ocultar la ventana principal que genera Tk
						messagebox.showinfo('Ayuda','[espacio] : iniciar búsqueda del camino.\n'
												'[click izq] : agregar inicio/objetivo/obstáculos\n'
												'[click der] : convertir una casilla a pasto.\n'
												'[c] : limpiar mapa actual.\n'
												'[n] : crear nuevo mapa.\n'
												'[+] : aumentar tamaño del mapa.\n'
												'[-] : disminuir tamaño del mapa.\n'
												'[h] : ayuda.\n'
										)
												
					# si se presiona alguna de las teclas: [n], [c], [+] ,[-] se actualizará la cuadricula.
					if evento.key == pygame.K_n or evento.key == pygame.K_c or evento.unicode == "-" or evento.unicode == "+":
						
						# en todo caso, se quitarán los nodos de inicio y fin
						inicio = None
						fin = None

						if evento.key == pygame.K_n or  evento.unicode == "-" or evento.unicode == "+":
							if evento.unicode == "-" or evento.unicode == "+":
								Tk().wm_withdraw() # para ocultar la ventana principal que genera Tk
								if evento.unicode == "-":
									
									if self.indice_dim > 0: # validar para que no se trate de acceder con indice negativo a DIMENSIONES_POSIBLES
										self.indice_dim -= 1 # disminiuir el valor de indice_dim para que apunte a un valor menor de DIMENSIONES_POSIBLES (menor número de casillas)
									else:
										messagebox.showinfo('Advertencia','Este es el número mínimo de casillas posibles')
										continue 
								if evento.unicode == "+":
									
									if self.indice_dim < len(self.DIMENSIONES_POSIBLES)-1: # validar para que no se trate de acceder a un indice mayor de los posibles en DIMENSIONES_POSIBLES
										self.indice_dim += 1 # aumentar el valor de indice_dim para que apunte a un valor mayor de DIMENSIONES_POSIBLES (mayor número de casillas)
									else:
										messagebox.showinfo('Advertencia','Este es el número máximo de casillas posibles')
										continue 

							filas =  self.DIMENSIONES_POSIBLES[self.indice_dim] #nuevo número de filas según el cambio en indice_dim
							mapa_actual = mapa.crear_mapa(filas) # crear un nuevo mapa en caso de las teclas de [n], [+] ,[-]

						cuadricula_actual = cuadricula.crearCuadricula(filas, self.ancho, mapa_actual) # actualizar con la nueva cuadricula

		pygame.quit() # terminar partida


	def obtenerPosicionDeClick(self, posicion, filas, ancho):
		"""
			Obtener la posición del nodo, (fila, columna), donde se hizo click en la cuadrícula.

			Parámetros
    		----------
			posicion: tuple
        		contiene la posición del pixel donde se hizo click => (x, y)
			filas: int
				número de filas que contiene la cuadrícula actual. Es uno de los valores de DIMENSIONES_POSIBLES.
			ancho: int
				tamaño, en píxeles, de la ventana de la partida.
		"""

		anchoCasilla = ancho // filas
		y, x = posicion

		fila = y // anchoCasilla
		columna = x // anchoCasilla

		return fila, columna
