import numpy as np
import math
import random
import matplotlib.pyplot as plt

pontos = []

numeroLados = random.randint(4, 10000)

for i in range(numeroLados):
    ponto = [random.randint(4, 10000),random.randint(4, 10000)]
    if ponto not in pontos: pontos.append(ponto)

xs = []
ys = []

for x,y in pontos:
    xs.append(x)
    ys.append(y)

def modulo(vetor2D: list) -> float:
    # Retorna o modulo de um vetor bidimensional
    return math.sqrt(vetor2D[0]**2 + vetor2D[1]**2)

def normaliza(vetor2D: list) -> list:
    # Retorna o vetor normalizado
    novoVetor = [vetor2D[0]/modulo(vetor2D), vetor2D[1]/modulo(vetor2D)]
    return novoVetor

def grahamScan(pontos: list) -> list:
    # Acha o casco convexo utilizando o algoritmo de Graham Scan
    
    primeiroPonto = min(pontos, key=lambda p: (p[1], p[0]))                                 # Achando o ponto com menor y e depois com menor x
    pontos.remove(primeiroPonto)                                                            # Retirando o ponto mais a esquerda e com menor y

    for ponto in pontos:                                                                    # Buscando os maiores angulos usando produto escalar
        vetorAngulo = normaliza([ponto[0] - primeiroPonto[0],ponto[1] - primeiroPonto[1]])
        dotProd = np.dot([-1,0], vetorAngulo)
        ponto.append(dotProd)
        
    pontos.sort(key=lambda x: (x[2], x[0]))                                                 # Ordenando em função dos ângulos e depois do x, como critério de desempate 
    segundoPonto = pontos.pop(0)                                                            # Retirando o ponto que forma o maior ângulo com o eixo x, pois este também estará no casco convexo
    convexHull = [primeiroPonto, segundoPonto[:2]]                                          # Iniciando meu casco convexo e retirando o terceiro argumento, utilizado para ordenação de ângulos
    
    for ponto in pontos:
        convexHull.append(ponto[:2])                                                        # Adicionando no casco convexo
        checkPonto = True                                                                   # Vendo se o ponto adicionado gera uma rotação no sentido horário, caso sim o produto vetorial seria negativo
        
        while checkPonto:
            vetor1 = [ponto[0] - convexHull[-2][0], ponto[1] - convexHull[-2][1]]
            vetor2 = [convexHull[-2][0] - convexHull[-3][0], convexHull[-2][1] - convexHull[-3][1]]
            vetProd = np.cross(vetor2,vetor1)
            if vetProd > 0: checkPonto = False
            else: 
                convexHull.remove(convexHull[-2])
                if len(convexHull) == 2: break                                              # Caso logo na primeira iteração ocorra 3 pontos colineares
    
    return convexHull

convex = grahamScan(pontos)
# Configurando o poligono para plot
convex = convex + [convex[0]]

xconvex = []
yconvex = []

for x,y in convex:
    xconvex.append(x)
    yconvex.append(y)

plt.plot(xconvex, yconvex)
plt.scatter(xs,ys)
plt.show()
    
