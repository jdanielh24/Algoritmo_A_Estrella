import pygame
import Colores as Color
pygame.init()

FONT_12 = pygame.font.SysFont('chalkduster.ttf', 12)
FONT_18 = pygame.font.SysFont('chalkduster.ttf', 18)
FONT_32 = pygame.font.SysFont('chalkduster.ttf', 32)


class Nodo:
	def __init__(self, fila, columna, ancho, total_filas):
		self.fila = fila
		self.columna = columna
		self.x = fila * ancho
		self.y = columna * ancho
		self.vecinos = []
		self.ancho = ancho
		self.total_filas = total_filas
		self.costo = 1
		self.f = "?"
		self.final = False

	def getF(self):
		return self.f

	def setF(self, f):
		self.f = f

	def getCosto(self):
		return self.costo

	def getPosicion(self):
		return self.fila, self.columna

	def crearMontania(self):
		self.color = self.colorMarco = Color.MONTANIA
		self.costo = 10

	def crearAgua(self):
		self.color = self.colorMarco = Color.AGUA
		self.costo = 20

	def crearBosque(self):
		self.color = self.colorMarco = Color.BOSQUE
		self.costo = 5

	def crearPasto(self):
		self.color = self.colorMarco = Color.PASTO
		self.costo = 1

	def esBarrera(self):
		return self.color == Color.NEGRO

	def esInicio(self):
		return self.color == Color.TURQUESA

	def esFinal(self):
		return self.final

	def reiniciar(self):
		self.crearPasto()
		self.final = False

	def crearInicio(self):
		self.color = self.colorMarco = Color.TURQUESA

	def crearCerrado(self):
		self.colorMarco = Color.ROJO

	def crearAbierto(self):
		self.colorMarco = Color.AZUL

	def crearBarrera(self):
		self.color = self.colorMarco = Color.NEGRO

	def crearFinal(self):
		self.colorCirculo = Color.ROSA
		self.final = True

	def crearCamino(self):
		self.colorMarco = Color.AMARILLO

	def dibujar(self, ventana):
		pygame.draw.rect(ventana, self.color,
		                 (self.x, self.y, self.ancho, self.ancho))
		margen_texto = ancho_marco = 2
		radio_circulo = 4

		if not self.esInicio():
			if self.total_filas < 16:
				margen_texto = ancho_marco = 7
				radio_circulo = 15
				obj_texto = FONT_32.render(str(self.getF()), True, Color.NEGRO)
			elif self.total_filas < 40:
				margen_texto = ancho_marco = 3
				radio_circulo = 7
				obj_texto = FONT_18.render(str(self.getF()), True, Color.NEGRO)
			else:
				obj_texto = FONT_12.render(str(self.getF()), True, Color.NEGRO)

			if self.esFinal():
				pygame.draw.circle(ventana, self.colorCirculo, (self.x +
				                   self.ancho/2, self.y + self.ancho/2), radio_circulo)

			pygame.draw.rect(ventana, self.colorMarco, (self.x, self.y,
			                 self.ancho, self.ancho), ancho_marco)
			ventana.blit(obj_texto, (self.x + margen_texto, self.y + margen_texto))

	def actualizarVecinos(self, cuadricula):
		self.vecinos = []
		if self.fila < self.total_filas - 1 and not cuadricula[self.fila + 1][self.columna].esBarrera(): # DOWN
			self.vecinos.append(cuadricula[self.fila + 1][self.columna])

		if self.fila > 0 and not cuadricula[self.fila - 1][self.columna].esBarrera(): # UP
			self.vecinos.append(cuadricula[self.fila - 1][self.columna])

		if self.columna < self.total_filas - 1 and not cuadricula[self.fila][self.columna + 1].esBarrera(): # RIGHT
			self.vecinos.append(cuadricula[self.fila][self.columna + 1])

		if self.columna > 0 and not cuadricula[self.fila][self.columna - 1].esBarrera(): # LEFT
			self.vecinos.append(cuadricula[self.fila][self.columna - 1])