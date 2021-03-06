# Algoritmo_A_Estrella

## Requisitos:
Python +3.0

Instalar PyGame: 

```pip install pygame```

## Ejecución
Acceder a la ruta donde se encuentra el proyecto y ejecutar el comando:

```python main.py```

## ¿Qué hace la aplicación?
Calcula el camino más corto entre el punto A (origen) y el punto B (objetivo o destino). En la cuadrícula, se cuenta con diferentes terrenos, los cuales tienen un costo asignado y este representa qué tan difícil o qué tan fácil es cruzar por ellos. Además, se pueden colocar obstáculos por los cuales no es posible pasar, por lo cual se deberá buscar una ruta que evite estos puntos.

## ¿Cómo funciona?
El algoritmo de búsqueda A* puede calcular caminos mínimos en una red, en este caso en un tablero o cuadrícula. El algoritmo es heurístico, por lo cual usa una evaluación heurística en la que mediante etiquetas (costos) de los nodos determina el camino óptimo.

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

### Pruebas
A continuación mostraremos una serie de pruebas que se realizaron con distintos mapas y cambiando la posición de los nodos de inicio, fin y objetivo.

Al final de cada ejecución, el programa nos muestra un cuadro de texto indicando el costo total del camino. Dicho costo, también es mostrado en la casilla donde se encuentra el objetivo.

Podemos hacer la comprobación haciendo la suma de los costos, viendo qué casillas forman parte del camino amarillo. Para ello, empleamos la siguiente fórmula:

![Fórmula](/img/formula.png)

donde: 

- CT = Costo total del camino final

- Si = Costo del suelo: S1 = 1 (Pasto), S2 = 5 (Bosque), S3 = 10 (Montaña), 
 S4 = 20 (Agua)

- ni = número de casillas del suelo Si. que forman parte del camino final.

La primera prueba será una cuadrícula de 10x10, con el propósito de observar bien que los cálculos se realizan correctamente. Agregamos el inicio, el objetivo y los obstáculos.

#### Prueba #1
Tablero de 10x10 casillas:

![Prueba 1-1](/img/4.png)

Resultado:

![Prueba 1-2](/img/5.png)

Al hacer la la suma empleando la fórmula indicada anteriormente, obtenemos:

- Pasto: 	S1 = 1, n1 = 5 : 	=>	1x5 = 5

- Bosque: 	S2 = 5, n2 = 4: 	=>	5x4 = 20

- Montaña: 	S3 = 10, n3 = 1:	=>	10x1 = 10

- Agua:	 	S4 = 20, n4 = 0: 	=>	20x0 = 0

CT = 5 + 20 + 10 + 0 

CT = 35

#### Prueba #2
Tablero de 25x25 casillas:

![Prueba 1-1](/img/6.png)

Resultado:

![Prueba 1-2](/img/7.png)

Al hacer la la suma empleando la fórmula indicada anteriormente, obtenemos:

- Pasto: 	S1 = 1, n1 = 47 : 	=>	1x47 = 47

- Bosque: 	S2 = 5, n2 = 0: 	=>	5x0 = 0

- Montaña: 	S3 = 10, n3 = 0:	=>	10x0 = 0

- Agua:	 	S4 = 20, n4 = 1: 	=>	20x1 = 20

CT = 47 + 0 + 0 + 20 

CT = 67

#### Prueba #3
Tablero de 40x40 casillas:

![Prueba 1-1](/img/8.png)

Resultado:

![Prueba 1-2](/img/9.png)

Al hacer la la suma empleando la fórmula indicada anteriormente, obtenemos:

- Pasto: 	S1 = 1, n1 = 26: 	=>	1x26 = 26

- Bosque: 	S2 = 5, n2 = 4: 	=>	5x4 = 20

- Montaña: 	S3 = 10, n3 = 1:	=>	10x1 = 10

- Agua:	 	S4 = 20, n4 = 0 	=>	20x0 = 0

CT = 26 + 20 + 10 + 0 

CT = 56
