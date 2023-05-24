import numpy as np
import random
import matplotlib.pyplot as plt

pontos = []

numeroLados = random.randint(4, 1000)

for i in range(numeroLados):
    ponto = [random.randint(4, 1000),random.randint(4, 1000)]
    if ponto not in pontos: pontos.append(ponto)

xs = []
ys = []

for x,y in pontos:
    xs.append(x)
    ys.append(y)
    
def divideNconquer(pontos: list, ordena: int = 0) -> list:
    '''Descobre o casco convexo usando o metodo divide and conquer'''
    if ordena: pontos.sort()                                                         # Ordena a lista inicial de pontos
    
    if len(pontos) > 3:
        esquerda, direita = divideNconquer(pontos[:int(len(pontos)/2)]), divideNconquer(pontos[int(len(pontos)/2):])        # Recursao
    elif len(pontos) == 3:                                                           # Organiza um triangulo no sentido horario
        convexHull = [pontos[0]]
        if np.cross(np.subtract(pontos[1], pontos[0]),
                    np.subtract(pontos[2], pontos[1])) > 0:
            convexHull.append(pontos[2])
            convexHull.append(pontos[1])
            return convexHull
        elif np.cross(np.subtract(pontos[1], pontos[0]),
                    np.subtract(pontos[2], pontos[1])) == 0:
            convexHull.append(pontos[2])
            return convexHull
        else: return pontos                                                          
             
    else: return pontos                                                              # Como os pontos ja estao ordenados, retorno apenas a lista com eles

    '''Inicio do processo de merge de dois cascos convexos'''
    esquerdaMax = 0
    indEsqFinal = 0
    for i,ponto in enumerate(esquerda):                                              # Descobrindo o pontos mais a direita do poligono a esquerda
        x = ponto[0]
        if x > esquerdaMax:
            esquerdaMax = x
            indEsqFinal = i
    
    '''Descobrindo a tangente superior externa'''
    indEsq = indEsqFinal
    indDir = 0
    ladoEsq = True                                                                   # Comeco pelo lado esquerdo
    tangenteCima = True
    parada = False                                                                   # Variavel que vai controlar o fim das iteracoes
    while tangenteCima:
        if ladoEsq:
            if np.cross(np.subtract(direita[indDir], esquerda[indEsq]),
                        np.subtract(direita[(indDir + 1) % len(direita)], direita[indDir])) > 0:
                indDir = (indDir + 1) % len(direita)
                parada = False
            else:                                                                    # Caso eu nao consiga prosseguir eu troco de lado
                ladoEsq = False
                if parada: tangenteCima = False
                parada = True
        else:
            if np.cross(np.subtract(esquerda[indEsq],direita[indDir]),
                     np.subtract(esquerda[indEsq-1],esquerda[indEsq])) < 0:
                indEsq -= 1
                parada = False
            else:
                ladoEsq = True
                if parada: tangenteCima = False
                parada = True
    corteEsqCima, corteDirCima = indEsq, indDir                                      # Pontos que pertencem a tangente superior externa
    
    '''Descobrindo a tangente inferior externa'''
    indEsq = indEsqFinal           
    indDir = 0
    ladoEsq = True
    tangenteBaixo = True
    parada = False
    while tangenteBaixo:
        if ladoEsq:
            if np.cross(np.subtract(direita[indDir], esquerda[indEsq]),
                        np.subtract(direita[indDir-1], direita[indDir])) < 0:
                indDir -= 1
                parada = False
            else:
                ladoEsq = False
                if parada: tangenteBaixo = False
                parada = True
        else:
            if np.cross(np.subtract(esquerda[indEsq],direita[indDir]),
                     np.subtract(esquerda[(indEsq+1) % len(esquerda)],esquerda[indEsq])) > 0:
                indEsq = (indEsq + 1) % len(esquerda)
                parada = False
            else:
                ladoEsq = True
                if parada: tangenteBaixo = False
                parada = True   
                
    corteEsqBaixo, corteDirBaixo = indEsq, indDir                                    # Pontos que pertencem a tangente inferior externa
    
    convexHull = []
    
    '''Criando o casco convexo a partir dos pontos de corte encontrados'''
    indAdd = 0
    while esquerda[indAdd] != esquerda[corteEsqCima]:
        convexHull.append(esquerda[indAdd])
        indAdd = (indAdd + 1) % len(esquerda)
        
    if esquerda[corteEsqCima] not in convexHull: convexHull.append(esquerda[corteEsqCima])
    
    indAdd = corteDirCima
    while direita[indAdd] != direita[corteDirBaixo]:
        convexHull.append(direita[indAdd])
        indAdd = (indAdd + 1) % len(direita)

    if direita[corteDirBaixo] not in convexHull: convexHull.append(direita[corteDirBaixo])
    
    indAdd = corteEsqBaixo  
    while esquerda[indAdd] != esquerda[0]:
        convexHull.append(esquerda[indAdd])
        indAdd = (indAdd + 1) % len(esquerda)
    
    return convexHull
    
convex = divideNconquer(pontos,1)

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