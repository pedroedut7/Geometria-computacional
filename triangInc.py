import numpy as np
import random
import matplotlib.pyplot as plt

pontos = []

numeroLados = random.randint(4, 100)

for i in range(numeroLados):
    pontos.append((random.randint(4, 100),random.randint(4, 100)))

xs = []
ys = []

for x,y in pontos:
    xs.append(x)
    ys.append(y)

def IncrementalAlgorithmTriang(pontos: list) -> list:
    pontosOrdenados = pontos  
    
    # Ordenando a lista
    pontosOrdenados.sort(reverse = True)                                            
    convexHull = [pontosOrdenados.pop()]
    triangulacoes = []
    
    # Escolhendo os primeiros pontos
    if np.cross(np.subtract(pontosOrdenados[-1], convexHull[0]),
                np.subtract(pontosOrdenados[-2], pontosOrdenados[-1])) > 0:
        convexHull.append(pontosOrdenados[-2])
        convexHull.append(pontosOrdenados[-1])
        pontosOrdenados.pop()
        pontosOrdenados.pop()
    elif np.cross(np.subtract(pontosOrdenados[-1], convexHull[0]),
                np.subtract(pontosOrdenados[-2], pontosOrdenados[-1])) == 0:
        convexHull.append(pontosOrdenados[-2])
        pontosOrdenados.pop()
        pontosOrdenados.pop()
    else:
        convexHull.append(pontosOrdenados.pop())
        convexHull.append(pontosOrdenados.pop())
    
    # Adicionando a primeira triangulacao
    triangulacoes.append(convexHull)                                                                        
    
    # Algoritmo incremental
    while pontosOrdenados:
        novoPonto = pontosOrdenados.pop()
        # Aresta que informará os pontos que eu consigo ver
        arestaSinal = []
        
        for i,pontoAtual in enumerate(convexHull):
            # Percorrendo o casco convexo em sentido horário
            proxElemento = convexHull[(i+1) % len(convexHull)]
            prodVet = np.cross([proxElemento[0] - pontoAtual[0], proxElemento[1] - pontoAtual[1]], 
                               [novoPonto[0] - proxElemento[0], novoPonto[1] - proxElemento[1]])
            # Verdade se consigo ver a aresta ou se os pontos estão na mesma linha 
            if prodVet < 0: arestaSinal.append(False)   
            elif prodVet == 0: arestaSinal.append(True)         
            else: arestaSinal.append(True) 
            
        # Escolhendo o lugar de adição do ponto
        pontosCorte = [1, len(arestaSinal)]
        acharTrue = True
        
        for i, sinal in enumerate(arestaSinal):
            if sinal and acharTrue: 
                pontosCorte[0] = i+1
                acharTrue = False
            elif (not sinal) and (not acharTrue):
                pontosCorte[1] = i
                break
            
        # Adicionando o ponto

        for i in range(pontosCorte[0] - 1, pontosCorte[1]):
            novoTriang = []
            novoTriang.append(convexHull[i])
            novoTriang.append(novoPonto)
            novoTriang.append(convexHull[(i+1) % len(convexHull)])
            triangulacoes.append(novoTriang)
            
        convexHull = convexHull[:pontosCorte[0]] + [novoPonto] + convexHull[pontosCorte[1]:]
    return triangulacoes

triangulacoes = IncrementalAlgorithmTriang(pontos)
# Configurando o poligono para plot
for triangulo in triangulacoes:
    convex = triangulo
    convex = convex + [convex[0]]

    xconvex = []
    yconvex = []
    for x,y in convex:
        xconvex.append(x)
        yconvex.append(y)
    
    plt.plot(xconvex, yconvex)
    
plt.scatter(xs,ys)
plt.show()
    