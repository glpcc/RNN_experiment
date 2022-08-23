from car_game.mapa import Mapa
from car_game.car import Coche
from network.network import Network
from copy import deepcopy
import numpy as np
import pygame
import json
import timeit

map_car_parameters = json.load(open("car_game/map.json"))

map = Mapa(map_car_parameters['mapa_interior'],map_car_parameters['mapa_exterior'],map_car_parameters['lineas_puntos'])
initial_car = Coche(
    [map_car_parameters['parametros_coche']['posicion_x'],map_car_parameters['parametros_coche']['posicion_y']],
    map_car_parameters['parametros_coche']['altura'],
    map_car_parameters['parametros_coche']['anchura'],
    map_car_parameters['parametros_coche']['rotacion_inicial'],
    map_car_parameters['parametros_coche']['potencia_aceleracion'],
    map_car_parameters['parametros_coche']['potencia_frenada'],
    map_car_parameters['parametros_coche']['potencia_rotacion']
)

num_cars = 50
cars_brains = [Network(num_inputs= 7, num_network_neurons= 50, num_outputs= 2,connection_type='random_connections') for _ in range(num_cars)]
cars = [deepcopy(initial_car) for _ in range(num_cars)]

pygame.init()
XMAX = 1500
YMAX = 1000
canvas = pygame.display.set_mode((XMAX,YMAX))
done = False
clock = pygame.time.Clock()
start_time = timeit.default_timer()
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] or timeit.default_timer() - start_time > 5:
        best_score = -1
        best_net = None
        for car,net in zip(cars,cars_brains):
            if car.puntos > best_score:
                best_score = car.puntos
                best_net = net
        print(best_score)
        if best_net is not None:
            cars_brains = [deepcopy(best_net) for _ in range(num_cars)]
            cars = [deepcopy(initial_car) for _ in range(num_cars)]
            for net in cars_brains[1:]:
                net.mutate(default_mutation_prob= 0.01, default_mutation_amount= 0.01)
        start_time = timeit.default_timer()



    canvas.fill((0,0,0))
    map.dibujar(canvas)
    for car,net in zip(cars,cars_brains):
        car.dibujar(canvas)
        # car.dibujar_sensores(canvas,map)
        inputs = np.array(car.calcular_distancia_sensores(map) + [car.velocidad_x,car.velocidad_y])
        outputs = np.tanh(net.run_step(inputs))
        if outputs[0] > 0:
            car.acelerar()
        elif outputs[0] < 0:
            car.frenar()
        if outputs[1] > 0.3 :
            car.rotar(True)
        elif outputs[1] < -0.3:
            car.rotar(False)
        car.actualizar(map)
        if car.comprobar_colisiones(map):
            cars.remove(car)
            cars_brains.remove(net)
    

    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
