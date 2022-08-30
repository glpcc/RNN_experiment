import math
import pygame
from car_game.mapa import Mapa
from car_game.utils import calcular_interseccion,calcular_distancia,comprobar_interseccion


class Coche():
    '''
    La clase coche tendra varias propiedades:
        posicion_y ,posicion_y : float -> Centro del coche
        altura, anchura : float -> La altura y anchura del coche
        rotacion : float -> Sera el angulo en radianes teniendo como cero la posicion vertical y la direccion positiva del angulo es hacia la dercha
        potencia : float -> Sera la capacidad de aceleracion del coche a mas potencia mas aceleracion 
        potencia_frenada : float -> como la potencia pero con la capacidad de frenada este ah de ser entre 0 y 1 (siendo 0 ninguna frenada y uno la para total)
        velocidad_x : float -> La velocidad en el eje x
        velocidad_y : float -> La velocidad en el eje y
        angulo_esquinas : float -> Este sera el angulo que forman las esquinas respecto al eje imaginario del coche que servira para dibujarlo
        distancia_al_centor : float -> es la distancia de la diagonal de las esquinas al punto
        rotacion : float -> es la rotacion del coche
    '''

    def __init__(self, posicion_inicial: list[int], altura: float, anchura: float, rotacion: float, potencia: float, potencia_frenada: float, potencia_rotacion: float) -> None:
        self.alive = True
        self.puntos = 0
        self.numero_de_vueltas = 0
        self.posicion_x = posicion_inicial[0]
        self.posicion_y = posicion_inicial[1]
        self.altura = altura
        self.anchura = anchura
        self.rotacion = rotacion
        self.potencia = potencia
        self.potencia_frenada = potencia_frenada
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.angulo_esquinas = math.atan((self.anchura/2)/(self.altura/2))
        self.distancia_al_centro = math.sqrt((self.anchura/2)**2 + (self.altura/2)**2)
        self.potencia_rotacion = potencia_rotacion
        # La lista puntos sera una lista con las coordenadas de los puntos en orden ArribaIzquierda,AD,AbajoD,AbajoI calculando las coordenadas
        # con el angulo del coche y el angulo de las esquinas mas la distancia del centro a las esquinas y luego restandolo o sumandoselo a la posicion del coche
        self.esquinas = [
            (math.sin(self.rotacion-self.angulo_esquinas)*self.distancia_al_centro + self.posicion_x, math.cos(self.rotacion-self.angulo_esquinas)*self.distancia_al_centro+self.posicion_y),
            (math.sin(self.rotacion+self.angulo_esquinas)*self.distancia_al_centro+self.posicion_x, math.cos(self.rotacion+self.angulo_esquinas)*self.distancia_al_centro+self.posicion_y),
            (math.sin(self.rotacion-self.angulo_esquinas+math.pi)*self.distancia_al_centro+self.posicion_x, math.cos(self.rotacion-self.angulo_esquinas+math.pi)*self.distancia_al_centro+self.posicion_y),
            (math.sin(self.rotacion+self.angulo_esquinas+math.pi)*self.distancia_al_centro+self.posicion_x, math.cos(self.rotacion+self.angulo_esquinas+math.pi)*self.distancia_al_centro+self.posicion_y)]
        # Ahora calculo los puntos del centro de los lados
        self.puntos_centro = [
            (math.sin(self.rotacion+math.pi)*(self.altura/2)+self.posicion_x, math.cos(self.rotacion+math.pi)*(self.altura/2)+self.posicion_y),
            (math.sin(self.rotacion+math.pi/2)*self.anchura/2+self.posicion_x,math.cos(self.rotacion+math.pi/2)*self.anchura/2+self.posicion_y),
            (math.sin(self.rotacion-math.pi/2)*self.anchura/2+self.posicion_x, math.cos(self.rotacion-math.pi/2)*self.anchura/2+self.posicion_y)]

    def rotar(self, direccion: bool) -> None:
        """
        Por razones de optimizacion he decidido que dirreccion == True signifa la izquierda y false la derecha
        """
        if direccion:
            self.rotacion -= 0.1
        else:
            self.rotacion += 0.1

    def acelerar(self, amount = 1) -> None:
        self.velocidad_y -= math.cos(self.rotacion)*self.potencia*amount
        self.velocidad_x -= math.sin(self.rotacion)*self.potencia*amount

    def frenar(self, amount = 1) -> None:
        self.velocidad_y *= 1 - self.potencia_frenada*amount
        self.velocidad_x *= 1 - self.potencia_frenada*amount

    def actualizar(self, mapa: Mapa) -> None:
        self.posicion_x += self.velocidad_x
        self.posicion_y += self.velocidad_y
        # Reduzco la velocidad para simular la friccion
        self.velocidad_y *= 0.97
        self.velocidad_x *= 0.97
        # Calculo los puntos de las cuatro esquinas del coche
        self.esquinas = [
            (math.sin(self.rotacion-self.angulo_esquinas)*self.distancia_al_centro + self.posicion_x, math.cos(self.rotacion-self.angulo_esquinas)*self.distancia_al_centro+self.posicion_y),
            (math.sin(self.rotacion+self.angulo_esquinas)*self.distancia_al_centro+self.posicion_x, math.cos(self.rotacion+self.angulo_esquinas)*self.distancia_al_centro+self.posicion_y),
            (math.sin(self.rotacion-self.angulo_esquinas+math.pi)*self.distancia_al_centro+self.posicion_x, math.cos(self.rotacion-self.angulo_esquinas+math.pi)*self.distancia_al_centro+self.posicion_y),
            (math.sin(self.rotacion+self.angulo_esquinas+math.pi)*self.distancia_al_centro+self.posicion_x, math.cos(self.rotacion+self.angulo_esquinas+math.pi)*self.distancia_al_centro+self.posicion_y)]
        # Actualizo los centros de los lados
        self.puntos_centro = [
            (math.sin(self.rotacion+math.pi)*(self.altura/2)+self.posicion_x, math.cos(self.rotacion+math.pi)*(self.altura/2)+self.posicion_y),
            (math.sin(self.rotacion+math.pi/2)*self.anchura/2+self.posicion_x,math.cos(self.rotacion+math.pi/2)*self.anchura/2+self.posicion_y),
            (math.sin(self.rotacion-math.pi/2)*self.anchura/2+self.posicion_x, math.cos(self.rotacion-math.pi/2)*self.anchura/2+self.posicion_y)]

        # Ahora calculo la puntuacion del coche
        for i in range(0, len(mapa.lineas_de_puntuaje)-1, 2):
            if self.puntos % (len(mapa.lineas_de_puntuaje)//2) == i//2:
                if comprobar_interseccion(mapa.lineas_de_puntuaje[i][0], mapa.lineas_de_puntuaje[i][1], mapa.lineas_de_puntuaje[i+1][0], mapa.lineas_de_puntuaje[i+1][1], self.posicion_x, self.posicion_y, self.puntos_centro[0][0], self.puntos_centro[0][1]):
                    self.puntos += 1
                    if self.puntos % 15 == 0:
                        self.numero_de_vueltas += 1

    
    def comprobar_colisiones(self, mapa: Mapa) -> bool:
        colisionado = False
        i = 0
        while not colisionado and i < len(mapa.circuito_exterior):
            for j in range(len(self.esquinas)):
                if comprobar_interseccion(self.esquinas[j][0], self.esquinas[j][1], self.esquinas[j-1][0], self.esquinas[j-1][1], mapa.circuito_exterior[i][0], mapa.circuito_exterior[i][1], mapa.circuito_exterior[i-1][0], mapa.circuito_exterior[i-1][1]):
                    colisionado = True
            i += 1
        i = 0
        while not colisionado and i < len(mapa.circuito_interior):
            for j in range(len(self.esquinas)):
                if comprobar_interseccion(self.esquinas[j][0], self.esquinas[j][1], self.esquinas[j-1][0], self.esquinas[j-1][1], mapa.circuito_interior[i][0], mapa.circuito_interior[i][1], mapa.circuito_interior[i-1][0], mapa.circuito_interior[i-1][1]):
                    colisionado = True
            i += 1

        return colisionado



    def calcular_sensores(self, mapa: Mapa) -> list[list[float]]:
        """
            En esta funcion calculo la interseccion de los segmentos formados desde el centro del coche a las esquinas y despues a los puntos centrales y elijo la que esta mas cerca del coche
            para asegurarme de que los sensores no atraviesan la pared
        """
        resultado = []
        for j in self.esquinas[2:]:
            intersecciones = []
            interseccion_ex = []
            for i in range(len(mapa.circuito_exterior)):
                #Este sera el segmento con el que compruebo la interseccion
                segmento = [mapa.circuito_exterior[i-1], mapa.circuito_exterior[i]]
                #Calculo la interseccion
                interseccion = calcular_interseccion(self.posicion_x, self.posicion_y, j[0], j[1], segmento[0][0], segmento[0][1], segmento[1][0], segmento[1][1])
                if interseccion != (-1, -1):
                    intersecciones += [interseccion]
            if intersecciones != []:
                interseccion_ex = self.interseccion_mas_cercana(intersecciones)

            intersecciones = []
            interseccion_in = []

            for k in range(len(mapa.circuito_interior)):
                segmento = [mapa.circuito_interior[k-1],mapa.circuito_interior[k]]
                interseccion = calcular_interseccion(self.posicion_x, self.posicion_y, j[0], j[1], segmento[0][0], segmento[0][1], segmento[1][0], segmento[1][1])
                if interseccion != (-1, -1):
                    intersecciones += [interseccion]

            if intersecciones != []:
                interseccion_in += self.interseccion_mas_cercana(
                    intersecciones)

            if interseccion_in != [] and interseccion_ex != []:
                resultado += [self.interseccion_mas_cercana(
                    [interseccion_in, interseccion_ex])]
            elif interseccion_ex != []:
                resultado += [interseccion_ex]
            elif interseccion_in != []:
                resultado += [interseccion_in]

        for j in self.puntos_centro:
            intersecciones = []
            interseccion_ex = []
            for i in range(len(mapa.circuito_exterior)):
                segmento = [mapa.circuito_exterior[i-1],
                            mapa.circuito_exterior[i]]
                interseccion = calcular_interseccion(
                    self.posicion_x, self.posicion_y, j[0], j[1], segmento[0][0], segmento[0][1], segmento[1][0], segmento[1][1])
                if interseccion != (-1, -1):
                    intersecciones += [interseccion]
            if intersecciones != []:
                interseccion_ex = self.interseccion_mas_cercana(intersecciones)

            intersecciones = []
            interseccion_in = []
            for k in range(len(mapa.circuito_interior)):
                segmento = [mapa.circuito_interior[k-1],
                            mapa.circuito_interior[k]]
                interseccion = calcular_interseccion(
                    self.posicion_x, self.posicion_y, j[0], j[1], segmento[0][0], segmento[0][1], segmento[1][0], segmento[1][1])
                if interseccion != (-1, -1):
                    intersecciones += [interseccion]

            if intersecciones != []:
                interseccion_in += self.interseccion_mas_cercana(intersecciones)

            if interseccion_in != [] and interseccion_ex != []:
                resultado += [self.interseccion_mas_cercana([interseccion_in, interseccion_ex])]
            elif interseccion_ex != []:
                resultado += [interseccion_ex]
            elif interseccion_in != []:
                resultado += [interseccion_in]
        return resultado

    def calcular_distancia_sensores(self, mapa: Mapa) -> list[float]:
        """
            En esta funcion calculo la distancia a la interseccion de los segmentos formados desde el centro del coche a las esquinas y despues a los puntos centrales y elijo la menor
            para asegurarme de que los sensores no atraviesan la pared

            La funcion es parecida a 
        """
        resultado = []
        for j in self.esquinas[2:]:
            intersecciones = []
            distancia_ex = 0
            for i in range(len(mapa.circuito_exterior)):
                segmento = [mapa.circuito_exterior[i-1],
                            mapa.circuito_exterior[i]]
                interseccion = calcular_interseccion(
                    self.posicion_x, self.posicion_y, j[0], j[1], segmento[0][0], segmento[0][1], segmento[1][0], segmento[1][1])
                if interseccion != (-1, -1):
                    intersecciones += [interseccion]
            if intersecciones != []:
                distancia_ex = self.distancia_minima(intersecciones)

            intersecciones = []
            distancia_in = 0
            for k in range(len(mapa.circuito_interior)):
                segmento = [mapa.circuito_interior[k-1],
                            mapa.circuito_interior[k]]
                interseccion = calcular_interseccion(
                    self.posicion_x, self.posicion_y, j[0], j[1], segmento[0][0], segmento[0][1], segmento[1][0], segmento[1][1])
                if interseccion != (-1, -1):
                    intersecciones += [interseccion]

            if intersecciones != []:
                distancia_in += self.distancia_minima(intersecciones)

            if distancia_in != 0 and distancia_ex != 0:
                resultado += [min([distancia_in, distancia_ex])]
            elif distancia_ex != 0:
                resultado += [distancia_ex]
            elif distancia_in != 0:
                resultado += [distancia_in]

        for j in self.puntos_centro:
            intersecciones = []
            distancia_ex = 0
            for i in range(len(mapa.circuito_exterior)):
                segmento = [mapa.circuito_exterior[i-1],
                            mapa.circuito_exterior[i]]
                interseccion = calcular_interseccion(
                    self.posicion_x, self.posicion_y, j[0], j[1], segmento[0][0], segmento[0][1], segmento[1][0], segmento[1][1])
                if interseccion != (-1, -1):
                    intersecciones += [interseccion]
            if intersecciones != []:
                distancia_ex = self.distancia_minima(intersecciones)

            intersecciones = []
            distancia_in = 0
            for k in range(len(mapa.circuito_interior)):
                segmento = [mapa.circuito_interior[k-1],
                            mapa.circuito_interior[k]]
                interseccion = calcular_interseccion(
                    self.posicion_x, self.posicion_y, j[0], j[1], segmento[0][0], segmento[0][1], segmento[1][0], segmento[1][1])
                if interseccion != (-1, -1):
                    intersecciones += [interseccion]

            if intersecciones != []:
                distancia_in += self.distancia_minima(intersecciones)

            if distancia_in != 0 and distancia_ex != 0:
                resultado += [min([distancia_in, distancia_ex])]
            elif distancia_ex != 0:
                resultado += [distancia_ex]
            elif distancia_in != 0:
                resultado += [distancia_in]

        return resultado

    
    def distancia_minima(self, lista_intersecciones):
        if len(lista_intersecciones) > 1:
            distancia_min = calcular_distancia(
                self.posicion_x, self.posicion_y, lista_intersecciones[0][0], lista_intersecciones[0][1])
            for k in lista_intersecciones[1:]:
                distancia = calcular_distancia(
                    self.posicion_x, self.posicion_y, k[0], k[1])
                if distancia < distancia_min:
                    distancia_min = distancia
            return distancia_min
        else:
            return calcular_distancia(self.posicion_x, self.posicion_y, lista_intersecciones[0][0], lista_intersecciones[0][1])

    
    
    def interseccion_mas_cercana(self, intersecciones):
        if len(intersecciones) > 1:
            distancia_min = calcular_distancia(
                self.posicion_x, self.posicion_y, intersecciones[0][0], intersecciones[0][1])
            intersecion_mas_cercana = intersecciones[0]
            for k in intersecciones[1:]:
                if calcular_distancia(self.posicion_x, self.posicion_y, k[0], k[1]) < distancia_min:
                    intersecion_mas_cercana = k
            return intersecion_mas_cercana
        else:
            return intersecciones[0]

    

    # Dibuja las lineas que actuan como sensores del coche
    def dibujar_sensores(self, canvas, mapa: Mapa) -> None:
        for i in self.calcular_sensores(mapa):
            pygame.draw.line(canvas, (255, 0, 255),
                             (self.posicion_x, self.posicion_y), i)

    #Dibujo el coche
    def dibujar(self, canvas) -> None:
        # Dibujo las lineas de los puntos
        pygame.draw.lines(canvas, (255, 255, 255), True, self.esquinas)
