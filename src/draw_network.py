import math
from random import random
from network.network import Network
import pygame
import numpy as np



class NetDrawer():
    def __init__(self, net: Network, square_x: int, square_y: int, square_px_size: int, neuron_diam: int):
        self.net = net
        self.square_x = square_x
        self.square_y = square_y
        self.square_px_size = square_px_size
        self.neuron_diam = neuron_diam
        self.square_size = math.ceil(math.sqrt(net.num_network_neurons))
        # Calculate the positions for all neurons
        # Obtain input neurons on the left
        self.inputs_positions = []
        neuron_x = square_x
        if net.num_inputs %2 == 0:
            for i in range(net.num_inputs):
                neuron_y = (square_px_size - (square_px_size/self.square_size))/2 - (net.num_inputs//2 - 0.5 - i)*(square_px_size/self.square_size)+ square_y
                self.inputs_positions.append((neuron_x,neuron_y))
        else:
            for i in range(net.num_inputs):
                neuron_y = (square_px_size - (square_px_size/self.square_size))/2 - ((net.num_inputs - 1)//2 - i)*(square_px_size/self.square_size)+ square_y
                self.inputs_positions.append((neuron_x,neuron_y))

        # Obtain output neurons on the right
        self.output_positions = []
        neuron_x = square_x + square_px_size + square_px_size/3
        if net.num_outputs %2 == 0:
            for i in range(net.num_outputs):
                neuron_y = (square_px_size - (square_px_size/self.square_size))/2 - (net.num_outputs//2 - 0.5 - i)*(square_px_size/self.square_size) + square_y
                self.output_positions.append((neuron_x,neuron_y))
        else:
            for i in range(net.num_outputs):
                neuron_y = (square_px_size - (square_px_size/self.square_size))/2 - ((net.num_outputs - 1)//2 - i)*(square_px_size/self.square_size)+ square_y
                self.output_positions.append((neuron_x,neuron_y))

        # Obtain pos of inner neurons
        self.inner_neurons_pos = []
        for i in range(self.square_size):
            for j in range(self.square_size):
                if (i*self.square_size)+j < net.num_network_neurons:
                    neuron_x = (square_px_size/self.square_size)*j + square_x + square_px_size/4
                    neuron_y = (square_px_size/self.square_size)*i + square_y
                    self.inner_neurons_pos.append((neuron_x,neuron_y))

    def draw(self, canvas):
        for i,line in enumerate(self.net.neuron_connections):
            for j,pos in enumerate(line):
                if pos == 1:
                    if i < self.net.num_inputs:
                        start_pos = self.inputs_positions[i]
                    elif i >= self.net.num_total_neurons - self.net.num_outputs:
                        start_pos = self.output_positions[i - (self.net.num_total_neurons - self.net.num_outputs)]
                    else:
                        start_pos = self.inner_neurons_pos[i - self.net.num_inputs - 1]

                    if j < self.net.num_inputs:
                        end_pos = self.inputs_positions[j]
                    elif j >= self.net.num_total_neurons - self.net.num_outputs:
                        end_pos = self.output_positions[j - (self.net.num_total_neurons - self.net.num_outputs)]
                    else:
                        end_pos = self.inner_neurons_pos[j - self.net.num_inputs - 1]
                    if self.net.activated_neurons[i]:
                        pygame.draw.line(canvas,(179, 24, 7), start_pos, end_pos)
        # Draw all neurons
        for i,pos in enumerate(self.output_positions):
            neuron_val = self.net.neuron_values[self.net.num_total_neurons - self.net.num_outputs + i ]
            if neuron_val > 0:
                color = (255 - self.neuron_value_to_255(neuron_val,10),255,0)
            else:
                color = (255,255 - self.neuron_value_to_255(-neuron_val,10),0)
            pygame.draw.circle(canvas, color , pos, self.neuron_diam)

        for i,pos in enumerate(self.inputs_positions):
            neuron_val = self.net.neuron_values[i]
            if neuron_val > 0:
                color = (255 - self.neuron_value_to_255(neuron_val,500),255,255 - self.neuron_value_to_255(neuron_val,500))
            else:
                color = (255,255 - self.neuron_value_to_255(-neuron_val,500),255 - self.neuron_value_to_255(-neuron_val,500))
            pygame.draw.circle(canvas, color , pos, self.neuron_diam)
        self.draw_neurons(canvas, self.inner_neurons_pos,self.net.activated_neurons[self.net.num_inputs:-self.net.num_outputs],color=(52, 235, 225), activated_color=(0, 255, 21), radius=self.neuron_diam)

    # Util
    def draw_neurons(self, canvas, positions,activation_matrix, color = (255,0,0),activated_color = (0,255,0), radius = 20):
        for pos,activated in zip(positions,activation_matrix):
            if activated:
                pygame.draw.circle(canvas, activated_color, pos, radius)
            else:
                pygame.draw.circle(canvas, color, pos, radius)

    def neuron_value_to_255(self,neuron_val: int, threshold = 20) -> int:
        if neuron_val < threshold:
            old_range = threshold
            new_range = 255 
            new_value = (neuron_val * new_range) / old_range
            return int(new_value)
        else:
            return 255