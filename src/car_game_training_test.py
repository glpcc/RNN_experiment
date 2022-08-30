from car_game.mapa import Mapa
from car_game.car import Coche
from network.network import Network
from copy import deepcopy
import pickle
import numpy as np
import pygame
import json
import timeit
import random

# UTIL FUNCTION
def load_map_and_car(params) -> tuple[Mapa,Coche]:
    return (Mapa(params['mapa_interior'],params['mapa_exterior'],params['lineas_puntos']),
    Coche(
    [params['parametros_coche']['posicion_x'],params['parametros_coche']['posicion_y']],
    params['parametros_coche']['altura'],
    params['parametros_coche']['anchura'],
    params['parametros_coche']['rotacion_inicial'],
    params['parametros_coche']['potencia_aceleracion'],
    params['parametros_coche']['potencia_frenada'],
    params['parametros_coche']['potencia_rotacion']
    ))


f1 = open("car_game/map2.json")
f2 = open("car_game/map.json")
map1_params = json.load(f1)
map2_params = json.load(f2)
f1.close()
f2.close()
maps_and_cars = [
    load_map_and_car(map1_params),
    load_map_and_car(map2_params)
 ]
current_map_index = random.randint(0,len(maps_and_cars)-1)
initial_car = maps_and_cars[current_map_index][1]
map = maps_and_cars[current_map_index][0]

num_cars = 50
cars_brains = [Network(num_inputs= 7, num_network_neurons= 50, num_outputs= 2,connection_type='random_connections', connection_probability=0.8) for _ in range(num_cars)]
cars = [deepcopy(initial_car) for _ in range(num_cars)]

pygame.init()
XMAX = 1500
YMAX = 1000
canvas = pygame.display.set_mode((XMAX,YMAX))
done = False
clock = pygame.time.Clock()
start_time = timeit.default_timer()
best_score = -1
best_net = None
waiting_time = 15
surviving_cars = 10
save_best = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] or timeit.default_timer() - start_time > waiting_time or cars == []:
        # Change the current map to see multimap performance (delete if not needed)
        current_map_index = random.randint(0,len(maps_and_cars)-1)
        initial_car = maps_and_cars[current_map_index][1]
        map = maps_and_cars[current_map_index][0]
        # Sort cars by performance
        sorted_cars_and_brains = [(car,net) for car,net in zip(cars,cars_brains)]
        sorted_cars_and_brains.sort(reverse= True,key= lambda k: k[0].puntos)
        if save_best:
            f = open("car_game/best_cars/car_brain_0.obj", 'wb')
            pickle.dump(sorted_cars_and_brains[0],f)
            f.close()
            save_best = False
        # Clean the values of the best nets
        for _,net in sorted_cars_and_brains[:surviving_cars]:
            net.clean_values()
        # Get the best scores
        best_scores = [i[0].puntos for i in sorted_cars_and_brains[:surviving_cars] ]
        print(best_scores)
        # Here i calculate the number of "childs" for each best car based on probabilites given by aplying softmax to the car points
        num_childs: np.ndarray = np.around((num_cars-surviving_cars)*(np.exp(best_scores)/np.sum(np.exp(best_scores)))) # type:ignore
        print(num_childs)
        cars = []
        cars_brains = []
        cars += [deepcopy(initial_car) for i in range(surviving_cars)]
        cars_brains += [i[1] for i in sorted_cars_and_brains[:surviving_cars]]
        for j,num in enumerate(num_childs):
            cars += [deepcopy(initial_car) for i in range(int(num))]
            new_car_brains = [deepcopy(sorted_cars_and_brains[j][1]) for i in range(int(num))]
            for net in new_car_brains:
                net.mutate(default_mutation_prob= 0.1, default_mutation_amount= 0.1/(best_scores[j]+1))
            cars_brains += new_car_brains

        start_time = timeit.default_timer()
    if keys[pygame.K_UP]:
        waiting_time += 0.1
        print(waiting_time)
    if keys[pygame.K_LEFT]:
        save_best = True

    canvas.fill((0,0,0))
    map.dibujar(canvas)
    for car,net in zip(cars,cars_brains):
        if car.alive:
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
                car.alive = False
    

    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
