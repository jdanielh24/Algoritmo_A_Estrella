from multiprocessing.connection import wait
from turtle import delay
import pygame, sys
import math
import random
from boton import Button
from queue import PriorityQueue


pygame.init()

anchoYAlto = 800
ventanaMenu = pygame.display.set_mode((anchoYAlto, anchoYAlto))
fondo_menu = pygame.image.load("fondoMenu.png")
ventana = pygame.display.set_mode((anchoYAlto, anchoYAlto))
pygame.display.set_caption("Proyecto IA algoritmo estrella")

ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 255, 0)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
MORADO = (128, 0, 128)
NARANJA = (255, 165 ,0)
GRIS = (128, 128, 128)
TURQUESA = (64, 224, 208)
MONTANIA = (139,69,19)
AGUA = (93, 173, 226)
BOSQUE = (25, 111, 61 )
PASTO = (125, 206, 160)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)


class Nodo:
	def __init__(self, fila, columna, anchoYAlto, total_filas):
		self.fila = fila
		self.columna = columna
		self.x = fila * anchoYAlto
		self.y = columna * anchoYAlto
		self.color = BLANCO
		self.vecinos = []
		self.anchoYAlto = anchoYAlto
		self.total_filas = total_filas
		self.costo = 1
	
	def getCosto(self):
		return self.costo

	def esMontania(self):
		return self.color == MONTANIA

	def crearMontania(self):
		self.color = MONTANIA
		self.costo = 50

	def esAgua(self):
		return self.color == AGUA

	def crearAgua(self):
		self.color = AGUA
		self.costo = 100
	
	def esBosque(self):
		return self.color == BOSQUE

	def crearBosque(self):
		self.color = BOSQUE
		self.costo = 10

	def esPasto(self):
		return self.color == PASTO

	def crearPasto(self):
		self.color = PASTO
		self.costo = 1

	def getPosicion(self):
		return self.fila, self.columna

	def estaCerrado(self):
		return self.color == ROJO

	def estaAbierto(self):
		return self.color == VERDE

	def esBarrera(self):
		return self.color == NEGRO

	def esInicio(self):
		return self.color == NARANJA

	def esFinal(self):
		return self.color == TURQUESA

	def reiniciar(self):
		self.color = BLANCO

	def crearInicio(self):
		self.color = NARANJA

	def crearCerrado(self):
		self.color = ROJO

	def crearAbierto(self):
		self.color = VERDE

	def crearBarrera(self):
		self.color = NEGRO

	def crearFinal(self):
		self.color = TURQUESA

	def crearCamino(self):
		self.color = MORADO

	def dibujar(self, ventana):
		pygame.draw.rect(ventana, self.color, (self.x, self.y, self.anchoYAlto, self.anchoYAlto))

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

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruirCamino(provieneDe, actual, dibujar):
	while actual in provieneDe:
		actual = provieneDe[actual]
		actual.crearCamino()
		dibujar()


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
			reconstruirCamino(provieneDe, fin, dibujar)
			fin.crearFinal()
			return True

		for vecino in actual.vecinos:
			g_temporal = g[actual] + vecino.getCosto()
			if g_temporal < g[vecino]:
				provieneDe[vecino] = actual
				g[vecino] = g_temporal
				f[vecino] = g_temporal + h(vecino.getPosicion(), fin.getPosicion())
				if vecino not in listaAbiertaHash:
					contador += 1
					listaAbierta.put((f[vecino], contador, vecino))
					listaAbiertaHash.add(vecino)
					vecino.crearAbierto()
		dibujar()

		if actual != inicio:
			actual.crearCerrado()
		
	return False 


def crearCuadricula(filas, anchoYAlto):
	cuadricula = []
	anchoCasilla = anchoYAlto // filas
	mapa = crear_mapa(filas)
	for i in range(filas):
		cuadricula.append([])
		for j in range(filas):
			nodo = Nodo(i, j, anchoCasilla, filas)
			if (mapa[i][j] == 'P'):
				nodo.crearPasto()
			if (mapa[i][j] == 'B'):
				nodo.crearBosque()
			if (mapa[i][j] == 'M'):
				nodo.crearMontania()
			if (mapa[i][j] == 'A'):
				nodo.crearAgua()
			cuadricula[i].append(nodo)

	return cuadricula


def dibujarCuadricula(ventana, filas, anchoYAlto):
	anchoCasilla = anchoYAlto // filas
	for i in range(filas):
		pygame.draw.line(ventana, GRIS, (0, i * anchoCasilla), (anchoYAlto, i * anchoCasilla))
		for j in range(filas):
			pygame.draw.line(ventana, GRIS, (j * anchoCasilla, 0), (j * anchoCasilla, anchoYAlto))


def dibujar(ventana, cuadricula, filas, anchoYAlto):
	ventana.fill(BLANCO)

	for fila in cuadricula:
		for nodo in fila:
			nodo.dibujar(ventana)

	dibujarCuadricula(ventana, filas, anchoYAlto)
	pygame.display.update()

def obtenerPosicionDeClick(posicion, filas, anchoYAlto):
	anchoCasilla = anchoYAlto // filas
	y, x = posicion

	fila = y // anchoCasilla
	columna = x // anchoCasilla

	return fila, columna

def anadir_suelo_contiguo(mapa,  i, j, prob, tipo_suelo):
    if prob < 0:
        return
    
    if(random.random() < prob):
        mapa [i][j] = tipo_suelo
    
    if (i-1 >= 0 and j-1 >= 0) and (i+1 < len(mapa) and j+1 < len(mapa)):
        anadir_suelo_contiguo(mapa,  i-1,   j,      prob-0.1, tipo_suelo)
        anadir_suelo_contiguo(mapa,  i,     j-1,    prob-0.1, tipo_suelo)
        anadir_suelo_contiguo(mapa,  i,     j+1,    prob-0.1, tipo_suelo)
        anadir_suelo_contiguo(mapa,  i+1,   j,      prob-0.1, tipo_suelo)
    
    return

def anadirSuelos(mapa):
    SUELOS = ['B', 'M', 'A']
    PESOS = [0.5, 0.3, 0.2 ]
    
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if (random.random() > 0.97):
                suelo = random.choices(population=SUELOS, weights=PESOS, k=1)[0]
                mapa[i][j] = suelo
                anadir_suelo_contiguo(mapa, i, j, 0.5, suelo)


def crear_mapa(ancho):
	mapa = []
	for i in range(ancho):
		mapa.append([])
		for j in range(ancho):
			mapa[i].append('P')
	anadirSuelos(mapa)
	return mapa

'''
def crear_mapa(X):
	mapa = [ ['P','M','M','M','M','M','M','M','M','M'],
			 ['P','P','P','M','M','M','P','P','P','P'],
			 ['P','P','P','A','M','M','P','A','A','P'],
			 ['P','P','P','A','A','M','P','A','A','P'],
			 ['P','P','P','A','A','M','P','M','A','P'],
			 ['P','P','M','M','M','M','P','P','A','P'],
			 ['M','M','M','M','M','M','P','P','P','P'],
			 ['M','P','P','P','P','P','P','P','P','P'],
			 ['M','P','P','P','P','P','P','P','M','M'],
			 ['M','P','P','P','P','M','M','M','M','M'],
			]
	return mapa
	'''
def dibujarMenu():
	while True:
		ventanaMenu.blit(fondo_menu, (0, 0))
		posicionMouse = pygame.mouse.get_pos()
		textoMenu = get_font(100).render("MENU", True, BLANCO)
		contenedorTextoMenu = textoMenu.get_rect(center=(300, 100))
		botonJugar = Button(image=pygame.image.load("rectangulo.png"), pos=(300, 230), 
                            text_input="Jugar", font=get_font(30), base_color=BLANCO, hovering_color=VERDE)
		botonControles= Button(image=pygame.image.load("rectangulo.png"), pos=(300, 380), 
                            text_input="Controles", font=get_font(30), base_color=BLANCO, hovering_color=VERDE)
		botonSalir = Button(image=pygame.image.load("rectangulo.png"), pos=(300, 530), 
                            text_input="Salir", font=get_font(30), base_color=BLANCO, hovering_color=VERDE)

		ventanaMenu.blit(textoMenu, contenedorTextoMenu)
		for button in [botonJugar, botonControles, botonSalir]:
			button.changeColor(posicionMouse)
			button.update(ventanaMenu)
			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if botonJugar.checkForInput(posicionMouse):
					main(ventana, anchoYAlto)
				if botonControles.checkForInput(posicionMouse):
					controles()
				if botonSalir.checkForInput(posicionMouse):
					pygame.quit()
					sys.exit()
		pygame.display.update()

def controles():
	while True:
		mousePosicion = pygame.mouse.get_pos()  
		ventanaMenu.fill(NEGRO)
		texto = get_font(40).render("Controles", True, BLANCO)
		textoControles = get_font(30).render("C: Reiniciar",True,BLANCO)
		textoControles2 = get_font(25).render("Espacio: Buscar camino",True,BLANCO)
		contenedorTexto = texto.get_rect(center=(300, 150))
		contenedorTextoControles = textoControles.get_rect(center=(300,250))
		contenedorTextoControles2= textoControles2.get_rect(center=(300,350))
		ventanaMenu.blit(texto, contenedorTexto)
		ventanaMenu.blit(textoControles,contenedorTextoControles)
		ventanaMenu.blit(textoControles2,contenedorTextoControles2)
		regresarBtn = Button(image=None, pos=(300, 450), 
						text_input="Atras", font=get_font(40), base_color=BLANCO, hovering_color=VERDE)
		regresarBtn.changeColor(mousePosicion)
		regresarBtn.update(ventanaMenu)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if regresarBtn.checkForInput(mousePosicion):
					dibujarMenu()
		pygame.display.update()

def main(ventana, anchoYAlto):
	filas = 50
	cuadricula = crearCuadricula(filas, anchoYAlto)

	inicio = None
	fin = None

	run = True
	while run:
		dibujar(ventana, cuadricula, filas, anchoYAlto)
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				posicion = pygame.mouse.get_pos()
				fila, columna = obtenerPosicionDeClick(posicion, filas, anchoYAlto)
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
				fila, columna = obtenerPosicionDeClick(posicion, filas, anchoYAlto)
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

					algoritmo(lambda: dibujar(ventana, cuadricula, filas, anchoYAlto), cuadricula, inicio, fin)

				if evento.key == pygame.K_c:
					inicio = None
					fin = None
					cuadricula = crearCuadricula(filas, anchoYAlto)

	pygame.quit()


dibujarMenu()
#main(ventana, anchoYAlto)