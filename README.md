# Algoritmo_A_Estrella

## Requisitos:
Python +3.0

Instalar PyGame: 

```pip install pygame```

## Ejecución
Acceder a la ruta donde se encuentra el proyecto y ejecutar el comando:

```python main.py```

## ¿Cómo funciona?
El algoritmo de búsqueda A* puede calcular caminos mínimos en una red, en este caso en un tablero o cuadrícula, el algoritmo es heurístico por lo cual usa una evaluación heurística en la que mediante etiquetas (costos) de los nodos determina el camino óptimo.

La función con la que se calcula el camino es la siguiente

 > f(n) = g(n) + h(n)

donde:

> g(n) es la distancia del camino desde el origen s al n.

> h(n) es la distancia estimada desde el nodo n hasta el nodo destino t.

Cada vez que el sistema inicia, se crea un mundo con una distribución aleatoria de los suelos. El mundo se conforma de una cuadrícula de NxN, donde cada casilla tiene un tipo de suelo.

### Tipos de suelo
![tipos de suelo](/img/1.png)

### Otros elementos
![elementos](/img/2.png)

Un ejemplo de cómo se ve un mundo recién creado es el siguiente:
![ejemplo de mapa](/img/3.png)
