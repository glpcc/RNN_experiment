import math
from network.network import Network
import pygame
import pickle

# Utils
def draw_circles(canvas, positions, color = (0,255,0), radius = 20):
    for pos in positions:
        pygame.draw.circle(canvas, color, pos, radius)


pygame.init()
XMAX = 1500
YMAX = 1000
f1 = open('car_game/best_cars/car_brain_01.obj','rb')
# net: Network = pickle.load(f1)[1]
net: Network = Network(num_inputs= 7, num_network_neurons= 10, num_outputs= 3,connection_type='random_connections', connection_probability=1)

f1.close()
canvas = pygame.display.set_mode((XMAX,YMAX))
done = False
clock = pygame.time.Clock()
# Not actual total px occupied by the network drawing
square_px_size = 300
neuron_diam = 10
square_x = 50
square_y = 50
square_size = math.ceil(math.sqrt(net.num_network_neurons))
print(square_size)

# Calculate the positions for all neurons
# Obtain input neurons on the left
inputs_positions = []
neuron_x = square_x
if net.num_inputs %2 == 0:
    for i in range(net.num_inputs):
        neuron_y = (square_px_size - (square_px_size/square_size))/2 - (net.num_inputs//2 - 0.5 - i)*(square_px_size/square_size)+ square_y
        inputs_positions.append((neuron_x,neuron_y))
else:
    for i in range(net.num_inputs):
        neuron_y = (square_px_size - (square_px_size/square_size))/2 - ((net.num_inputs - 1)//2 - i)*(square_px_size/square_size)+ square_y
        inputs_positions.append((neuron_x,neuron_y))

# Obtain output neurons on the right
output_positions = []
neuron_x = square_x + square_px_size + square_px_size/3
if net.num_outputs %2 == 0:
    for i in range(net.num_outputs):
        neuron_y = (square_px_size - (square_px_size/square_size))/2 - (net.num_outputs//2 - 0.5 - i)*(square_px_size/square_size) + square_y
        output_positions.append((neuron_x,neuron_y))
else:
    for i in range(net.num_outputs):
        neuron_y = (square_px_size - (square_px_size/square_size))/2 - ((net.num_outputs - 1)//2 - i)*(square_px_size/square_size)+ square_y
        output_positions.append((neuron_x,neuron_y))

# Obtain pos of inner neurons
inner_neurons_pos = []
for i in range(square_size):
    for j in range(square_size):
        if (i*square_size)+j < net.num_network_neurons:
            neuron_x = (square_px_size/square_size)*j + square_x + square_px_size/4
            neuron_y = (square_px_size/square_size)*i + square_y
            inner_neurons_pos.append((neuron_x,neuron_y))

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    for i,line in enumerate(net.neuron_connections):
        for j,pos in enumerate(line):
            if pos == 1:
                if i < net.num_inputs:
                    start_pos = inputs_positions[i]
                elif i >= net.num_total_neurons - net.num_outputs:
                    start_pos = output_positions[i - (net.num_total_neurons - net.num_outputs)]
                else:
                    start_pos = inner_neurons_pos[i - net.num_inputs - 1]

                if j < net.num_inputs:
                    end_pos = inputs_positions[j]
                elif j >= net.num_total_neurons - net.num_outputs:
                    end_pos = output_positions[j - (net.num_total_neurons - net.num_outputs)]
                else:
                    end_pos = inner_neurons_pos[j - net.num_inputs - 1]

                pygame.draw.line(canvas,(255,0,0), start_pos, end_pos)
    
    
    # Draw all neurons
    draw_circles(canvas,  output_positions, color=(0,255,0), radius=neuron_diam)
    draw_circles(canvas, inputs_positions, color=(0,255,0), radius=neuron_diam)
    draw_circles(canvas, inner_neurons_pos, color=(0,255,0), radius=neuron_diam)

    

    keys = pygame.key.get_pressed()
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

