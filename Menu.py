"""
Archivo: menu.py

	Este archivo contiene lo necesario para crear el menú inicial de la aplicación.  

	Importaciones:
		> pygame: módulo que permite la creación de videojuegos en dos dimensiones.
		> sys: módulo que provee acceso a funciones y objetos mantenidos por del intérprete.
		> colores: módulo que provee un conjunto de diferentes colores en formato RGB.
		> juego: módulo para crear la ventana que inicia la partida con el buscador de caminos.
		> boton: módulo para crear botones.
"""

import pygame
import sys
import colores as color
from juego import Juego
from boton import Button

class Menu:
	"""
		Clase utilizada para crear un menú.

		Atributos
    	----------
    	ANCHO : int
        	resolución, en pixeles, que tendrá la ventana.
    	ventanaMenu : pygame.Surface
        	objeto que representa la ventana del menú.
    	fondoMenu : pygame.Surface
        	objeto utilizado para cargar la imagen de fondo.
    	ventanaPartida : pygame.Surface
        	objeto que representa la ventana para la partida.
	"""

	ANCHO = 800
	ventanaMenu = pygame.display.set_mode((ANCHO, ANCHO))
	fondoMenu = pygame.image.load("fondoMenu.jpg")
	ventanaPartida = pygame.display.set_mode((ANCHO, ANCHO))


	def __init__(self):
		"""
			Inicializar el menú con un título para la ventana.
		"""
		
		pygame.display.set_caption("Proyecto IA algoritmo estrella")


	def get_font(self, size):
		"""
			Obtener un objeto Font.

			Parámetros
    		----------
			size: int
				tamaño de la fuente.
		"""
		
		return pygame.font.Font("font.ttf", size)


	def iniciar(self):
		"""
			Iniciar el menú principal de la aplicación.
		"""
		
		while True:
			self.ventanaMenu.blit(self.fondoMenu, (0, 0)) # poner fondoMenu sobre ventanaMenu en la posicion (0,0)
			posicionMouse = pygame.mouse.get_pos() # posicionMouse = (x, y)
			
			# crear textoMenu, obtener un objeto Rect de él y almacenarlo en contenedorTextoMenu:
			textoMenu = self.get_font(100).render("MENU", True, color.BLANCO)
			contenedorTextoMenu = textoMenu.get_rect(center=(400, 200)) # center=(x,y) => centrar en dicha posicion.
			
			# crear los 3 botones siguientes:
			botonJugar = Button(image=pygame.image.load("rectangulo.png"), pos=(400, 330),
                        text_input="Jugar", font=self.get_font(30), base_color=color.BLANCO, hovering_color=color.VERDE)
			botonControles = Button(image=pygame.image.load("rectangulo.png"), pos=(400, 480),
                            text_input="Controles", font=self.get_font(30), base_color=color.BLANCO, hovering_color=color.VERDE)
			botonSalir = Button(image=pygame.image.load("rectangulo.png"), pos=(400, 630),
                            text_input="Salir", font=self.get_font(30), base_color=color.BLANCO, hovering_color=color.VERDE)

			self.ventanaMenu.blit(textoMenu, contenedorTextoMenu) # agregar título en VentanaMenu.
			
			# cambiar el color de los botones cuando el cursor se encuentre sobre ellos.
			for button in [botonJugar, botonControles, botonSalir]:
				button.changeColor(posicionMouse)
				button.update(self.ventanaMenu)

			# manejo de eventos (acciones con mouse o teclado):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					# terminar aplicación
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					# si uno de los botones es presionado:
					if botonJugar.checkForInput(posicionMouse):
						# iniciar una partida
						partida = Juego(self.ventanaPartida, self.ANCHO)
						partida.ejecutar()
					if botonControles.checkForInput(posicionMouse):
						# mostrar ventana de controles
						self.controles()
					if botonSalir.checkForInput(posicionMouse):
						# terminar aplicación
						pygame.quit()
						sys.exit()

			pygame.display.update() #mostrar ventana 


	def controles(self):
		"""
			Desplegar la ventana de controles.
		"""

		while True:
			self.ventanaMenu.blit(self.fondoMenu, (0, 0))  # poner fondoMenu sobre ventanaMenu en la posicion (0,0)
			mousePosicion = pygame.mouse.get_pos() # posicionMouse = (x, y)
			
			texto = self.get_font(40).render("Controles", True, color.BLANCO) # título
			textoControles = [] # contendrá 
			
			# contiene las indicaciones para cada tecla
			leyendas_controles = ("C: Limpiar mapa actual", "N: Crear nuevo mapa", "+: aumentar tamaño del mapa", "Click der: convertir una casilla a pasto",
                              "Click izq: agregar inicio/objetivo/obstáculos", "Espacio: iniciar búsqueda del camino", "H: ayuda")
			
			# agregar cada leyenda como objeto Rect en textoControles
			for leyenda in leyendas_controles:
				textoControles.append(self.get_font(17).render(leyenda, True, color.BLANCO))

			contenedorTexto = texto.get_rect(center=(400, 70))
			contenedorTextoControles = []

			y = 170 # valor inicial en 'y' donde se empezará a poner el texto
			for i in range(7): # son 7 leyendas
				contenedorTextoControles.append(textoControles[i].get_rect(center=(400, y)))
				y += 50 # dejar espacio de 50px entre cada leyenda

			self.ventanaMenu.blit(texto, contenedorTexto)

			# agregar los objetos que contienen las leyendas en ventanaMenu
			for i in range(len(textoControles)):
				self.ventanaMenu.blit(textoControles[i], contenedorTextoControles[i])
			
			# crear botón para regresar
			regresarBtn = Button(image=None, pos=(400, 600),
                             text_input="Atras", font=self.get_font(40), base_color=color.BLANCO, hovering_color=color.VERDE)
			regresarBtn.changeColor(mousePosicion)
			regresarBtn.update(self.ventanaMenu)
			
			# manejo de eventos (acciones con mouse o teclado):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					# terminar aplicación
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if regresarBtn.checkForInput(mousePosicion):
						# volver a crear la ventana de menú principal
						self.iniciar()
			
			pygame.display.update() 