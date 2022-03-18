from tkinter import *
from tkinter import messagebox
from multiprocessing.connection import wait
from turtle import delay
import pygame, sys
import random
from boton import Button
from queue import PriorityQueue


pygame.init()

DIMENSIONES_POSIBLES = [4, 6, 8, 10, 16, 20, 25, 32, 40, 50, 80, 100]
indice_dim = 9
ANCHO = 800
ventanaMenu = pygame.display.set_mode((ANCHO, ANCHO))
fondo_menu = pygame.image.load("fondoMenu.jpg")
ventana = pygame.display.set_mode((ANCHO, ANCHO))
pygame.display.set_caption("Proyecto IA algoritmo estrella. Tablero de " + str(DIMENSIONES_POSIBLES[indice_dim]) + "x" + str(DIMENSIONES_POSIBLES[indice_dim]) + " casillas" )

costo_total = 0

ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
MORADO = (128, 0, 128)
NARANJA = (255, 135 ,0)
GRIS = (128, 128, 128)
TURQUESA = (0, 253, 255)
MONTANIA = (139,69,19)
AGUA = (93, 173, 226)
BOSQUE = (25, 111, 61 )
PASTO = (125, 206, 160)

FONT_12 = pygame.font.SysFont('chalkduster.ttf', 12)
FONT_16 = pygame.font.SysFont('chalkduster.ttf', 16)
FONT_32 = pygame.font.SysFont('chalkduster.ttf', 32)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)


class Nodo:
	def __init__(self, fila, columna, ANCHO, total_filas):
		self.fila = fila
		self.columna = columna
		self.x = fila * ANCHO
		self.y = columna * ANCHO
		self.color = BLANCO
		self.vecinos = []
		self.ANCHO = ANCHO
		self.total_filas = total_filas
		self.costo = 1
		self.colorMarco = BLANCO
	
	def getCosto(self):
		return self.costo

	def esMontania(self):
		return self.color == MONTANIA

	def crearMontania(self):
		self.color = self.colorMarco = MONTANIA
		self.costo = 10

	def esAgua(self):
		return self.color == AGUA

	def crearAgua(self):
		self.color = self.colorMarco = AGUA
		self.costo = 20
	
	def esBosque(self):
		return self.color == BOSQUE

	def crearBosque(self):
		self.color = self.colorMarco = BOSQUE
		self.costo = 5

	def esPasto(self):
		return self.color == PASTO

	def crearPasto(self):
		self.color = self.colorMarco = PASTO
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

	def esCamino(self):
		return self.color == AMARILLO

	def reiniciar(self):
		self.crearPasto()

	def crearInicio(self):
		self.color = MORADO
		self.colorMarco = self.color

	def crearCerrado(self):
		self.colorMarco = ROJO

	def crearAbierto(self):
		self.colorMarco = AZUL

	def crearBarrera(self):
		self.color = NEGRO
		self.colorMarco = self.color

	def crearFinal(self):
		self.color = TURQUESA
		self.colorMarco = self.color

	def crearCamino(self):
		self.color
		self.colorMarco = AMARILLO

	def dibujar(self, ventana):
		margen_texto = 1
		pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ANCHO, self.ANCHO))
		if indice_dim < 4:
			pygame.draw.rect(ventana, self.colorMarco, (self.x, self.y, self.ANCHO, self.ANCHO), 7)
			obj_texto = FONT_32.render(str(self.costo), True, NEGRO)
			margen_texto = 12
		elif indice_dim < 10:
			pygame.draw.rect(ventana, self.colorMarco, (self.x, self.y, self.ANCHO, self.ANCHO), 3)
			obj_texto = FONT_16.render(str(self.costo), True, NEGRO)
			margen_texto = 3
		else:
			pygame.draw.rect(ventana, self.colorMarco, (self.x, self.y, self.ANCHO, self.ANCHO), 2)
			obj_texto = FONT_12.render(str(self.costo), True, NEGRO)
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

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruirCamino(provieneDe, actual, dibujar):
	global costo_total 
	costo_total = 0
	while actual in provieneDe:
		actual = provieneDe[actual]
		actual.crearCamino()
		dibujar()
		costo_total += actual.getCosto()


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


def crearCuadricula(filas, ANCHO, mapa):
	cuadricula = []
	anchoCasilla = ANCHO // filas

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


def dibujarCuadricula(ventana, filas, ANCHO):
	anchoCasilla = ANCHO // filas
	for i in range(filas):
		pygame.draw.line(ventana, GRIS, (0, i * anchoCasilla), (ANCHO, i * anchoCasilla))
		for j in range(filas):
			pygame.draw.line(ventana, GRIS, (j * anchoCasilla, 0), (j * anchoCasilla, ANCHO))


def dibujar(ventana, cuadricula, filas, ANCHO):
	#ventana.fill(BLANCO)

	for fila in cuadricula:
		for nodo in fila:
			nodo.dibujar(ventana)

	dibujarCuadricula(ventana, filas, ANCHO)
	pygame.display.update()

def obtenerPosicionDeClick(posicion, filas, ANCHO):
	anchoCasilla = ANCHO // filas
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

def dibujarMenu():
	while True:
		ventanaMenu.blit(fondo_menu, (0, 0))
		posicionMouse = pygame.mouse.get_pos()
		textoMenu = get_font(100).render("MENU", True, BLANCO)
		contenedorTextoMenu = textoMenu.get_rect(center=(400, 200))
		botonJugar = Button(image=pygame.image.load("rectangulo.png"), pos=(400, 330), 
                            text_input="Jugar", font=get_font(30), base_color=BLANCO, hovering_color=VERDE)
		botonControles= Button(image=pygame.image.load("rectangulo.png"), pos=(400, 480), 
                            text_input="Controles", font=get_font(30), base_color=BLANCO, hovering_color=VERDE)
		botonSalir = Button(image=pygame.image.load("rectangulo.png"), pos=(400, 630), 
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
					main(ventana, ANCHO)
				if botonControles.checkForInput(posicionMouse):
					controles()
				if botonSalir.checkForInput(posicionMouse):
					pygame.quit()
					sys.exit()
		pygame.display.update()

def controles():
	while True:
		ventanaMenu.blit(fondo_menu, (0, 0))
		mousePosicion = pygame.mouse.get_pos()  
		texto = get_font(40).render("Controles", True, BLANCO)
		textoControles = []
		leyendas_controles = ("C: Limpiar mapa actual", "N: Crear nuevo mapa", "+: aumentar tamaño del mapa", "Click der: convertir una casilla a pasto",
					"Click izq: agregar inicio/objetivo/obstáculos", "Espacio: iniciar búsqueda del camino", "H: ayuda")
		for leyenda in leyendas_controles:
			textoControles.append(get_font(17).render(leyenda, True, BLANCO))

		contenedorTexto = texto.get_rect(center=(400, 70))
		contenedorTextoControles = []

		y = 170
		for i in range(7):
			contenedorTextoControles.append(textoControles[i].get_rect(center=(400, y)))
			y += 50

		ventanaMenu.blit(texto, contenedorTexto)
		for i in range(len(textoControles)):
			ventanaMenu.blit(textoControles[i], contenedorTextoControles[i])
		regresarBtn = Button(image=None, pos=(400, 600),  
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

def main(ventana, ANCHO):
	global indice_dim 
	indice_dim = 9
	filas = DIMENSIONES_POSIBLES[indice_dim]
	mapa = crear_mapa(filas)
	cuadricula = crearCuadricula(filas, ANCHO, mapa)

	inicio = None
	fin = None

	run = True

	Tk().wm_withdraw() #to hide the main window
	messagebox.showinfo('¡Importante!', 'Presiona la tecla [h] si deseas ver los controles.')

	while run:
		dibujar(ventana, cuadricula, filas, ANCHO)
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				posicion = pygame.mouse.get_pos()
				fila, columna = obtenerPosicionDeClick(posicion, filas, ANCHO)
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
				fila, columna = obtenerPosicionDeClick(posicion, filas, ANCHO)
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
					if algoritmo(lambda: dibujar(ventana, cuadricula, filas, ANCHO), cuadricula, inicio, fin):
						messagebox.showinfo('Éxito','¡Camino encontrado con éxito!\nCosto total: ' + str(costo_total) )
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
								if indice_dim < len(DIMENSIONES_POSIBLES)-1:
									indice_dim += 1
								else:
									messagebox.showinfo('Advertencia','Este es el número máximo de casillas posibles')
									continue
							pygame.display.set_caption("Proyecto IA algoritmo estrella. Tablero de " + str(DIMENSIONES_POSIBLES[indice_dim]) + "x" + str(DIMENSIONES_POSIBLES[indice_dim]) + " casillas" )
						filas =  DIMENSIONES_POSIBLES[indice_dim]
						mapa = crear_mapa(filas)
					cuadricula = crearCuadricula(filas, ANCHO, mapa)

	pygame.quit()


dibujarMenu()
#main(ventana, ANCHO)