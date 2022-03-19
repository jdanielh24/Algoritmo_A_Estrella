import random

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