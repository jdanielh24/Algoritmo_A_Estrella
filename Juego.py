import pygame
from tkinter import *
from tkinter import messagebox
import Mapa
import Cuadricula 
import A_Estrella

#pygame.init()

class Juego:

	def __init__(self, ventana, ancho):
		self.ventana = ventana
		self.ancho = ancho
		self.DIMENSIONES_POSIBLES = [4, 6, 8, 10, 16, 20, 25, 32, 40, 50]
		self.indice_dim = 9

	def ejecutar(self):
		filas = self.DIMENSIONES_POSIBLES[indice_dim]
		
		mapa = Mapa.crear_mapa(filas)
		cuadricula = Cuadricula.crearCuadricula(filas, self.ancho, mapa)

		inicio = None
		fin = None

		run = True

		Tk().wm_withdraw() #to hide the main window
		messagebox.showinfo('¡Importante!', 'Asegurate de hacer click en la ventana del juego.\nPresiona la tecla [h] si deseas ver los controles.')
		
		while run:
			pygame.display.set_caption("Proyecto IA algoritmo estrella. Tablero de " + str(self.DIMENSIONES_POSIBLES[indice_dim]) + "x" + str(self.DIMENSIONES_POSIBLES[indice_dim]) + " casillas" )
			Cuadricula.dibujar(self.ventana, cuadricula, filas, self.ancho)
			for evento in pygame.event.get():
				if evento.type == pygame.QUIT:
					run = False

				if pygame.mouse.get_pressed()[0]: # LEFT
					posicion = pygame.mouse.get_pos()
					fila, columna = self.obtenerPosicionDeClick(posicion, filas, self.ancho)
					nodo = cuadricula[fila][columna]
					if not inicio and nodo != fin:
						inicio = nodo
						inicio.crearInicio()

					elif not fin and nodo != inicio:
						fin = nodo
						fin.crearFinal()

					elif nodo != fin and nodo != inicio:
						nodo.crearBarrera()

				elif pygame.mouse.get_pressed()[2]: # RIGHT
					posicion = pygame.mouse.get_pos()
					fila, columna = self.obtenerPosicionDeClick(posicion, filas, self.ancho)
					nodo = cuadricula[fila][columna]
					nodo.reiniciar()
					if nodo == inicio:
						inicio = None
					elif nodo == fin:
						fin = None

				if evento.type == pygame.KEYDOWN:
					if evento.key == pygame.K_SPACE and inicio and fin:
						for fila in cuadricula:
							for nodo in fila:
								nodo.actualizarVecinos(cuadricula)
					
						Tk().wm_withdraw() #to hide the main window
						if A_Estrella.algoritmo(lambda: Cuadricula.dibujar(self.ventana, cuadricula, filas, self.ancho), cuadricula, inicio, fin):
							messagebox.showinfo('Éxito','¡Camino encontrado con éxito!\nCosto total: ' + str(fin.getF()) )
						else:
							messagebox.showinfo('Error','No existe solución')
				
					if evento.key == pygame.K_h:
						Tk().wm_withdraw() #to hide the main window
						messagebox.showinfo('Ayuda','[espacio] : iniciar búsqueda del camino.\n'
												'[click izq] : agregar inicio/objetivo/obstáculos\n'
												'[click der] : convertir una casilla a pasto.\n'
												'[c] : limpiar mapa actual.\n'
												'[n] : crear nuevo mapa.\n'
												'[+] : aumentar tamaño del mapa.\n'
												'[-] : disminuir tamaño del mapa.\n'
												'[h] : ayuda.\n'
										)
												

					if evento.key == pygame.K_n or evento.key == pygame.K_c or evento.unicode == "-" or evento.unicode == "+":
						inicio = None
						fin = None
						if evento.key == pygame.K_n or  evento.unicode == "-" or evento.unicode == "+":
							if evento.unicode == "-" or evento.unicode == "+":
								Tk().wm_withdraw() #to hide the main window
								if evento.unicode == "-":
									if indice_dim > 0:
										indice_dim -= 1
									else: 
										messagebox.showinfo('Advertencia','Este es el número mínimo de casillas posibles')
										continue
								if evento.unicode == "+":
									if indice_dim < len(self.DIMENSIONES_POSIBLES)-1:
										indice_dim += 1
									else:
										messagebox.showinfo('Advertencia','Este es el número máximo de casillas posibles')
										continue
							filas =  self.DIMENSIONES_POSIBLES[indice_dim]
							mapa = Mapa.crear_mapa(filas)
						cuadricula = Cuadricula.crearCuadricula(filas, self.ancho, mapa)

		pygame.quit()

	def obtenerPosicionDeClick(self, posicion, filas, ancho):
		anchoCasilla = ancho // filas
		y, x = posicion

		fila = y // anchoCasilla
		columna = x // anchoCasilla

		return fila, columna
