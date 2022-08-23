import math
import json


#Funcion que devuelve una lista sin el elemento en el indice dado
def eliminar_indice_lista(lista: list,indice: int)-> list:
    nueva_lista = []
    for i in range(len(lista)):
        if i!= indice:
            nueva_lista += [lista[i]]
    
    return nueva_lista



#Calcula el punto de interseccion de dos rectas que solo tiene que estar dentro del segundo segmento
def calcular_interseccion(x1, y1, x2, y2, x3, y3, x4, y4) -> tuple[float, float]:
    # Calculo de interseccion a partir de dos puntos en cada segmento
    denominador = ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    u = ((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2))/denominador
    # En este caso si el valor de u no esta entre 0 y 1 signfica que la interseccion no esta dentro del segundo segmento
    if (not (0 <= u <= 1)):
        return (-1, -1)
    else:
        inter_x = x3+u*(x4-x3)
        inter_y = y3+u*(y4-y3)
        if calcular_distancia(inter_x, inter_y, x1, y1) > calcular_distancia(inter_x, inter_y, x2, y2):
            return (inter_x, inter_y)
        else:
            return (-1, -1)


#Calculo la distancia entre dos puntos
def calcular_distancia(x1, y1, x2, y2) -> float:
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)


#Comprueba si existe un punto de interseccion dentro de los dos segmentos
def comprobar_interseccion(x1, y1, x2, y2, x3, y3, x4, y4):
    # Calculo de interseccion a partir de dos puntos en cada segmento
    denominador = ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    u = ((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2))/denominador
    t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/denominador
    # En este caso si el valor de u/denominador esta entre 0 y 1  y t/denominador tambien lo esta signica que hay un punto de interseccion dentro de los dos segmentos
    if 0 <= t <= 1 and 0 <= u <= 1:
        return True
    else:
        return False




def multiplicacion_matrices(matriz1,matriz2):
    matriz_resultado = []
    if len(matriz1) == len(matriz2):
        for i in range(len(matriz1)):
            matriz_resultado += [matriz1[i]*matriz2[i]]
    
    return matriz_resultado


def suma_matrices(matriz1,matriz2):
    matriz_resultado = []
    if len(matriz1) == len(matriz2):
        for i in range(len(matriz1)):
            matriz_resultado += [matriz1[i]+matriz2[i]]
    
    return matriz_resultado

def suma_lista(lista):
    resultado = 0
    for i in lista:
        resultado += i
    return resultado
    
def menu(num_opciones: int)-> int:
    respondido = False
    while not respondido:
        respuesta = input('Introduzca su eleccion> ')
        for i in range(num_opciones+1):
            if respuesta == str(i):
                respuesta = i
                respondido = True

        if not respondido:
            print('Respuesta incorrecta por favor vuelva a intentarlo:')        
    return respuesta