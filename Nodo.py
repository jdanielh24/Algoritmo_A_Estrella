"""
Archivo: nodo.py

	Este archivo contiene la clase Nodo, utilizada para almacenar los atributos de cada casilla en la cuadrícula
	(tipo, color, costos, posición, vecinos etc).

	Importaciones:
		> pygame: módulo que permite la creación de videojuegos en dos dimensiones.
		> módulo que provee un conjunto de diferentes colores en formato RGB.
"""

import pygame
import colores as Color

pygame.init() # si se omite, no se crearán las fuentes. Se necesitan inicializar

# crear fuentes con distintos tamaños
FONT_12 = pygame.font.SysFont('chalkduster.ttf', 12)
FONT_18 = pygame.font.SysFont('chalkduster.ttf', 18)
FONT_32 = pygame.font.SysFont('chalkduster.ttf', 32)


class Nodo:
	"""
		Clase utilizada para almacenar los atributos de cada casilla en la cuadricula.
	"""

	def __init__(self, fila, columna, ancho, total_filas):
		"""
			Inicializar valores del nodo.

			Parámetros
    		----------
			fila: int
        		fila en que se encuentra el nodo
			columna: int
				columna en que se encuentra el nodo
			ancho: int
        		ancho de la casilla del nodo
			total_filas: int
				numero de filas que hay en la cuadricula donde se encuentra el nodo.

			Otros atributos
    		----------
			x: int
        		posicion en el eje X donde se encuentra el nodo
			y: int
				posicion en el eje Y donde se encuentra el nodo
			vecinos: list
        		vecinos del nodo
			costo: int
				costo que cuesta moverse por ese nodo, dependiendo del tipo de suelo. Es utilizado para calcular G en a_estrella.py
			f: str / int	
				valor de f. Es utilizadoo en a_estrella.py para determinar el camino más corto.
			final: bool
				True si es el nodo de fin (objetivo), de lo contrario es False.
		"""
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
		"""
			Obtener valor de f		
		"""
		return self.f


	def setF(self, f):
		"""
			Establecer valor de f.

			Parámetros
    		----------
			f: int
        		valor f del nodo.			
		"""		
		self.f = f


	def getCosto(self):
		"""
			Obtener valor de costo		
		"""
		return self.costo


	def getPosicion(self):
		"""
			Obtener posición del nodo como una tupla => (fila, columna)		
		"""
		return self.fila, self.columna


	def crearMontania(self):
		"""
			Indicar que el nodo es montaña
		"""
		self.color = self.colorMarco = Color.MONTANIA
		self.costo = 10


	def crearAgua(self):
		"""
			Indicar que el nodo es agua	
		"""
		self.color = self.colorMarco = Color.AGUA
		self.costo = 20


	def crearBosque(self):
		"""
			Indicar que el nodo es bosque	
		"""
		self.color = self.colorMarco = Color.BOSQUE
		self.costo = 5


	def crearPasto(self):
		"""
			Indicar que el nodo es pasto	
		"""		
		self.color = self.colorMarco = Color.PASTO
		self.costo = 1


	def esBarrera(self):
		"""
			Utilizar para comprobar si el nodo es una barrera	
		"""
		return self.color == Color.NEGRO


	def esInicio(self):
		"""
			Utilizar para comprobar si el nodo es el de inicio	
		"""
		return self.color == Color.TURQUESA


	def esFinal(self):
		"""
			Utilizar para comprobar si el nodo es el de fin	(objetivo)
		"""
		return self.final


	def reiniciar(self):
		"""
			Indicar que el nodo es pasto	
		"""
		self.crearPasto()
		self.final = False


	def crearInicio(self):
		"""
			Indicar que el nodo es de inicio	
		"""
		self.color = self.colorMarco = Color.TURQUESA


	def crearCerrado(self):
		"""
			Indicar que el nodo está en la lista cerrada	
		"""
		self.colorMarco = Color.ROJO


	def crearAbierto(self):
		"""
			Indicar que el nodo está en la lista abierta	
		"""
		self.colorMarco = Color.AZUL


	def crearBarrera(self):
		"""
			Indicar que el nodo es una barrera	
		"""
		self.color = self.colorMarco = Color.NEGRO


	def crearFinal(self):
		"""
			Indicar que el nodo es de fin (objetivo)	
		"""
		self.colorCirculo = Color.ROSA
		self.final = True


	def crearCamino(self):
		"""
			Indicar que el nodo forma parte del camino final	
		"""
		self.colorMarco = Color.AMARILLO


	def dibujar(self, ventana):
		"""
			dibujar el nodo en la ventana.

			Parámetros
    		----------
			ventana: pygame.Surface
        		objeto que representa la ventana para la partida.			
		"""	
		
		pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho)) # dibujar el nodo con el color de acuerdo al tipo de suelo o si es de inicio, fin o barrera
		margen_texto = ancho_marco = 2  # margen para poner el costo (si es 0, quedará tapado por el marco) y el ancho del marco del nodo
		radio_circulo = 4 # radio para dibujar el objetivo

		# si es el nodo de inicio no se pondrá marco ni se le agregará texto.
		if not self.esInicio():
			# mientras menos filas haya, más grandes serán las casillas, por lo que se amplían los valores del tamaño de fuente, margen, ancho de marco, etc
			# mientras más filas haya, más pequeñas serán las casillas, por lo que se disminuyen los valores del tamaño de fuente, margen, ancho de marco, etc

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
				# si el nodo es de fin, dibujar el círculo que representa el objetivo
				pygame.draw.circle(ventana, self.colorCirculo, (self.x + self.ancho/2, self.y + self.ancho/2), radio_circulo)

			pygame.draw.rect(ventana, self.colorMarco, (self.x, self.y,self.ancho, self.ancho), ancho_marco) # dibujar marco
			ventana.blit(obj_texto, (self.x + margen_texto, self.y + margen_texto)) # agregar texto en casilla, puede ser: "?" o el valor de F


	def actualizarVecinos(self, cuadricula):
		"""
			Indicar cuáles son los nodos de cada vecino (por si existen barreras).
			Los vecinos se almacenan dentro de vecinos[]

			Parámetros
    		----------
			cuadricula: list
        		contiene todos los nodos que conforman la cuadricula			
		"""	
		self.vecinos = []
		
		# si el nodo vecino es una barrera, no se almacena
		if self.fila < self.total_filas - 1 and not cuadricula[self.fila + 1][self.columna].esBarrera(): # vecino de abajo
			self.vecinos.append(cuadricula[self.fila + 1][self.columna])

		if self.fila > 0 and not cuadricula[self.fila - 1][self.columna].esBarrera(): # vecino de arriba
			self.vecinos.append(cuadricula[self.fila - 1][self.columna])

		if self.columna < self.total_filas - 1 and not cuadricula[self.fila][self.columna + 1].esBarrera(): # vecino de la derecha
			self.vecinos.append(cuadricula[self.fila][self.columna + 1])

		if self.columna > 0 and not cuadricula[self.fila][self.columna - 1].esBarrera(): # vecino de la izquierda
			self.vecinos.append(cuadricula[self.fila][self.columna - 1])