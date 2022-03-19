import pygame
import sys
import Colores as Color
import Juego
from boton import Button

class Menu:
	def __init__(self):
		self.ancho = 800
		self.ventanaMenu = pygame.display.set_mode((self.ancho, self.ancho))
		self.fondo_menu = pygame.image.load("fondoMenu.jpg")
		self.ventana = pygame.display.set_mode((self.ancho, self.ancho))

	def get_font(self, size):  # Returns Press-Start-2P in the desired size
		return pygame.font.Font("font.ttf", size)

	def iniciar(self):
		while True:
			self.ventanaMenu.blit(self.fondo_menu, (0, 0))
			posicionMouse = pygame.mouse.get_pos()
			textoMenu = self.get_font(100).render("MENU", True, Color.BLANCO)
			contenedorTextoMenu = textoMenu.get_rect(center=(400, 200))
			botonJugar = Button(image=pygame.image.load("rectangulo.png"), pos=(400, 330),
                        text_input="Jugar", font=self.get_font(30), base_color=Color.BLANCO, hovering_color=Color.VERDE)
			botonControles = Button(image=pygame.image.load("rectangulo.png"), pos=(400, 480),
                            text_input="Controles", font=self.get_font(30), base_color=Color.BLANCO, hovering_color=Color.VERDE)
			botonSalir = Button(image=pygame.image.load("rectangulo.png"), pos=(400, 630),
                            text_input="Salir", font=self.get_font(30), base_color=Color.BLANCO, hovering_color=Color.VERDE)

			self.ventanaMenu.blit(textoMenu, contenedorTextoMenu)
			for button in [botonJugar, botonControles, botonSalir]:
				button.changeColor(posicionMouse)
				button.update(self.ventanaMenu)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if botonJugar.checkForInput(posicionMouse):
						partida = Juego.Juego(self.ventana, self.ancho)
						partida.iniciar()
					if botonControles.checkForInput(posicionMouse):
						self.controles()
					if botonSalir.checkForInput(posicionMouse):
						pygame.quit()
						sys.exit()
			pygame.display.update()

	def controles(self):
		while True:
			self.ventanaMenu.blit(self.fondo_menu, (0, 0))
			mousePosicion = pygame.mouse.get_pos()
			texto = self.get_font(40).render("Controles", True, Color.BLANCO)
			textoControles = []
			leyendas_controles = ("C: Limpiar mapa actual", "N: Crear nuevo mapa", "+: aumentar tamaño del mapa", "Click der: convertir una casilla a pasto",
                              "Click izq: agregar inicio/objetivo/obstáculos", "Espacio: iniciar búsqueda del camino", "H: ayuda")
			for leyenda in leyendas_controles:
				textoControles.append(self.get_font(17).render(leyenda, True, Color.BLANCO))

			contenedorTexto = texto.get_rect(center=(400, 70))
			contenedorTextoControles = []

			y = 170
			for i in range(7):
				contenedorTextoControles.append(textoControles[i].get_rect(center=(400, y)))
				y += 50

			self.ventanaMenu.blit(texto, contenedorTexto)
			for i in range(len(textoControles)):
				self.ventanaMenu.blit(textoControles[i], contenedorTextoControles[i])
			regresarBtn = Button(image=None, pos=(400, 600),
                             text_input="Atras", font=self.get_font(40), base_color=Color.BLANCO, hovering_color=Color.VERDE)
			regresarBtn.changeColor(mousePosicion)
			regresarBtn.update(self.ventanaMenu)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if regresarBtn.checkForInput(mousePosicion):
						self.iniciar()
			pygame.display.update()