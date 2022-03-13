import random

def crear_mapa():
    ANCHO = 10;
    mapa = []
    for i in range(ANCHO):
        mapa.append([])
        for j in range(ANCHO):
            mapa[i].append('V')
    return mapa

def anadir_suelo_contiguo(mapa,  i, j, prob, tipo_suelo):
    if prob < 0:
        return
    
    if(random.random() < prob):
        mapa [i][j] == tipo_suelo
    
    if (i-1 >= 0 and j-1 >= 0) and (i+1 < len(mapa) and j+1 < len(mapa)):
        anadir_suelo_contiguo(mapa,  i-1,   j,      prob-0.1, tipo_suelo)
        anadir_suelo_contiguo(mapa,  i,     j-1,    prob-0.1, tipo_suelo)
        anadir_suelo_contiguo(mapa,  i,     j+1,    prob-0.1, tipo_suelo)
        anadir_suelo_contiguo(mapa,  i+1,   j,      prob-0.1, tipo_suelo)
    
    return

def anadirSuelos(mapa):
    SUELOS = ['B', 'M', 'A']
    PESOS = [0.6, 0.3, 0.1 ]
    
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            # print(random.random())
            if (random.random() > 0.5):
                suelo = random.choices(population=SUELOS, weights=PESOS, k=1)[0]
                mapa[i][j] = suelo
                anadir_suelo_contiguo(mapa, i, j, 0.5, suelo)

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