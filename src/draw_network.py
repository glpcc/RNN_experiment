import math
from network.network import Network
import pygame
import pickle

pygame.init()
XMAX = 1500
YMAX = 1000
f1 = open('car_game/best_cars/car_brain_01.obj','rb')
# net: Network = pickle.load(f1)[1]
net: Network = Network(num_inputs= 7, num_network_neurons= 50, num_outputs= 2,connection_type='random_connections', connection_probability=0.1)

f1.close()
canvas = pygame.display.set_mode((XMAX,YMAX))
done = False
clock = pygame.time.Clock()
square_px_size = 400
neuron_diam = 10
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    square_size = math.ceil(math.sqrt(net.num_total_neurons))
    for i,line in enumerate(net.neuron_connections):
        for j,pos in enumerate(line):
            if pos == 1:
                pygame.draw.line(canvas,(255,0,0), (i%square_size * (square_px_size/square_size) + 50, i//square_size * (square_px_size/square_size) + 50), (j%square_size * (square_px_size/square_size) + 50, j//square_size * (square_px_size/square_size) + 50))
    for i in range(square_size):
        for j in range(square_size):
            if (i*square_size)+j <= net.num_total_neurons:
                pygame.draw.circle(canvas,(0,255,0),(((square_px_size/square_size)*j + 50),(square_px_size/square_size)*i + 50),neuron_diam)
    

    keys = pygame.key.get_pressed()
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
