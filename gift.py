import numpy as np
import math
import random
import matplotlib.pyplot as plt

pontos = []

numeroLados = random.randint(4, 10000)

for i in range(numeroLados):
    pontos.append((random.randint(4, 10000),random.randint(4, 10000)))

xs = []
ys = []

for x,y in pontos:
    xs.append(x)
    ys.append(y)

def modulo(vetor2D: tuple) -> float:
    # Retorna o modulo de um vetor bidimensional
    return math.sqrt(vetor2D[0]**2 + vetor2D[1]**2)

def normaliza(vetor2D: tuple) -> tuple:
    # Retorna o vetor normalizado
    novoVetor = (vetor2D[0]/modulo(vetor2D), vetor2D[1]/modulo(vetor2D))
    return novoVetor

def giftWrapping(pontos: list) -> list:
    # Pega o ponto mais a esquerda (com menor x) e, a partir deste, inicia o algoritmo
    refPonto = min(pontos)                                                            # Ponto em que o algoritmo está rodando
    primeiroPonto = min(pontos)
    vetorCompair = [0,1]                                                              # Vetor de comparação inicial
    proxPonto = ()                                                                    # Indica o proximo ponto do casco
    ultimoPonto = ()                                                                  # Para evitar que o algoritmo entre em loop
    vetorAssociado = []                                                               # Vetor associado a minha ultima aresta do casco convexo
    convexHull = [refPonto]
    while(proxPonto != primeiroPonto):
        maiorProduto = -1                                                             # Usado para procurar o maior angulo (usando produto escalar)
        
        for ponto in pontos:
            if (ponto != ultimoPonto) and (ponto != convexHull[-1]):
                vetor = normaliza((ponto[0] - refPonto[0],                            #type: ignore
                                   ponto[1] - refPonto[1]))                           #type: ignore
                dotProd = np.dot([vetor[0], vetor[1]],
                                vetorCompair)
                if dotProd > maiorProduto: 
                    maiorProduto = dotProd
                    vetorAssociado = vetor
                    proxPonto = ponto

        vetorCompair = [vetorAssociado[0],
                        vetorAssociado[1]]
        refPonto = proxPonto
        ultimoPonto = convexHull[-1]
        convexHull.append(refPonto)
        
    return convexHull


convex = giftWrapping(pontos)
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
        
    