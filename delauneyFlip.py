import math
import numpy as np
import random
import matplotlib.pyplot as plt

pontos = []

numeroLados = random.randint(4, 100)

for i in range(numeroLados):
    ponto = [random.uniform(4, 100),random.uniform(4, 100)]
    if ponto not in pontos: pontos.append(ponto)

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

def circunf(triangulo: list) -> tuple:
    '''Dados 3 pontos, acha a circunferencia'''
    x, y, z = triangulo
    delta = 2 * (x[0] * (y[1] - z[1]) + y[0] * (z[1] - x[1]) + z[0] *  (x[1] - y[1]))
    h = ((x[0]**2 + x[1]**2) * (y[1] - z[1]) +  (y[0]**2 + y[1]**2) * (z[1] - x[1]) + (z[0]**2 + z[1]**2) *  (x[1] - y[1])) / delta
    k = ((x[0]**2 + x[1]**2) * (z[0] - y[0]) +  (y[0]**2 + y[1]**2) * (x[0] - z[0]) + (z[0]**2 + z[1]**2) *  (y[0] - x[0])) / delta
    r = math.sqrt((x[0] - h)**2 +  (x[1] - k)**2)
    return (h, k, r)

def inverter(triang1: list, triang2: list, iSub1: int) -> tuple:
    '''Troca as arestas caso necessario'''
    pontoDif1 = []
    pontoDif2 = []
    h,k,r = circunf(triang1)
    
    for ponto in triang1:
        if ponto not in triang2:
            pontoDif1 = ponto
            break
    for i, ponto in enumerate(triang2):
        if ponto not in triang1:
            pontoDif2 = ponto
        if ponto == triang1[iSub1-1]:
            iSub2 = i
            
        
    if ((pontoDif2[0] - h)**2 + (pontoDif2[1] - k)**2) <= r**2:                             # Caso o ponto esteja no circulo, e necessario troca as arestas
        triang1[iSub1] = pontoDif2
        triang2[iSub2] = pontoDif1
        
    return (triang1, triang2)

def delauneyFlip(triangulacoes: list) -> list:
    '''Encontra a triangulacao delauney, a partir de uma triangulacao qualquer'''
    i = 0
    while i != len(triangulacoes):
        j = 0
        while j != len(triangulacoes):
            if i != j:                                                                      # Procurando triangulos com uma aresta em comum
                x, y, z = triangulacoes[i]
                if x in triangulacoes[j] and y in triangulacoes[j]:
                    triangulacoes[i], triangulacoes[j] = inverter(triangulacoes[i], triangulacoes[j], 1)
                elif x in triangulacoes[j] and z in triangulacoes[j]:
                    triangulacoes[i], triangulacoes[j] = inverter(triangulacoes[i], triangulacoes[j], 0)
                elif y in triangulacoes[j] and z in triangulacoes[j]:
                    triangulacoes[i], triangulacoes[j] = inverter(triangulacoes[i], triangulacoes[j], 2)
                j += 1
                
            else: j += 1
        i += 1
    
    return triangulacoes

triangulacoes = delauneyFlip(IncrementalAlgorithmTriang(pontos))

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