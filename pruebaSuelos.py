import random

def crear_mapa():
    ANCHO = 10;
    mapa = []
    for i in range(ANCHO):
        mapa.append([])
        for j in range(ANCHO):
            mapa[i].append('V')
    return mapa

def anadirSuelos(mapa):
    SUELOS = ['B', 'M', 'A']
    PESOS = [0.6, 0.3, 0.1 ]
    
    for fila in mapa:
        for i in range(len(fila)):
            # print(random.random())
            if (random.random() > 0.8):
                fila[i] = random.choices(population=SUELOS, weights=PESOS, k=1)[0]
            #print(elem) 

    #if (random.random() > 0.8):
     #   nuevo)
    
    print(random.choices(population=SUELOS, weights=PESOS, k=10))

def imprimirMapa(mapa):
    for i in range(len(mapa)):
        print(str(i) + ': ' + str(mapa[i]))

def cambiandoValores(mapa):
    for fila in mapa:
        for i in range(len(fila)):
            fila[i] = 'X'
            

mapa = crear_mapa()
#cambiandoValores(mapa)
imprimirMapa(mapa)
anadirSuelos(mapa)
print()
imprimirMapa(mapa)

'''
    suelos = {'P': 0.6, 'B':0.25, 'M':0.1, 'A':0.05}

	mapa = [ ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M'],
			 ['G','M','M','M','M','M','M','M','M','M','G','M','M','M','M','M','M','M','M','M','G','M','M','M','M']
			]
    '''