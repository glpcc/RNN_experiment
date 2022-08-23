import pygame


class Mapa():
    """
    La clase mapa tendra el trazado del circuito asi como los metodos para comprobar colisiones y distancias
    
    """
    def __init__(self,circuito_interior: list[list[int]],circuito_exterior: list[list[int]], score_lines: list[list[int]]) -> None:
        self.circuito_interior = circuito_interior
        self.circuito_exterior = circuito_exterior
        self.lineas_de_puntuaje = score_lines



    def dibujar(self,canvas):
        pygame.draw.lines(canvas,(255,255,255),True,self.circuito_exterior)
        pygame.draw.lines(canvas,(255,255,255),True,self.circuito_interior)
        for i in range(0,len(self.lineas_de_puntuaje)-1,2):
            pygame.draw.line(canvas,(0,0,255),self.lineas_de_puntuaje[i],self.lineas_de_puntuaje[i+1])
