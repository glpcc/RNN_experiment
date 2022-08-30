from car_game.mapa import Mapa
from car_game.car import Coche
from network.network import Network
from draw_network import NetDrawer
from copy import deepcopy
import pickle
import numpy as np
import pygame
import json
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

def main():
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

    num_cars = 40
    cars_brains = [Network(num_inputs= 7, num_network_neurons= 49, num_outputs= 2,connection_type='random_connections', connection_probability=0.8, symetric_neuron_connections=False) for _ in range(num_cars)]
    cars = [deepcopy(initial_car) for _ in range(num_cars)]

    # Load the net drawer
    net_drawer = NetDrawer(cars_brains[0],20,20,200,5)
    pygame.init()
    XMAX = 1500
    YMAX = 1000
    canvas = pygame.display.set_mode((XMAX,YMAX))
    done = False
    clock = pygame.time.Clock()
    waiting_time = 10
    surviving_cars = 10
    save_best = False
    frames = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] or frames > waiting_time*60 or cars == []:
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
            # Reset the drawer to the best
            net_drawer = NetDrawer(sorted_cars_and_brains[0][1],20,20,200,5)
            # Get the best scores
            best_scores = [i[0].puntos for i in sorted_cars_and_brains[:surviving_cars] ]
            # Here i calculate the number of "childs" for each best car based on probabilites given by aplying softmax to the car points
            num_childs: np.ndarray = np.around((num_cars-surviving_cars)*(np.exp(best_scores)/np.sum(np.exp(best_scores)))) # type:ignore
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
            frames = 0
        if keys[pygame.K_UP]:
            waiting_time += 0.1
            print(waiting_time)
        if keys[pygame.K_LEFT]:
            save_best = True

        canvas.fill((0,0,0))
        map.dibujar(canvas)
        net_drawer.draw(canvas)
        for car,net in zip(cars,cars_brains):
            if car.alive:
                car.dibujar(canvas)
                # car.dibujar_sensores(canvas,map)
                inputs = np.array(car.calcular_distancia_sensores(map) + [car.velocidad_x,car.velocidad_y])
                outputs = np.tanh(net.run_step(inputs))
                if outputs[0] > 0:
                    car.acelerar(amount=outputs[0])
                elif outputs[0] < 0:
                    car.frenar(amount=-outputs[0])
                if outputs[1] > 0.3 :
                    car.rotar(True)
                elif outputs[1] < -0.3:
                    car.rotar(False)
                car.actualizar(map)
                if car.comprobar_colisiones(map):
                    car.alive = False
        frames += 1
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

if __name__ == '__main__':
    main()