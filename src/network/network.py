import numpy as np


class Network:
    def __init__(self, num_inputs, num_outputs, num_network_neurons):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.num_network_neurons = num_network_neuronsksysguard update
        # Make just a local variable if not needed
        self.num_total_neurons = num_inputs + num_network_neurons + num_outputs
        self.neuron_values = np.zeros(total_neurons)
        self.activated_neurons = np.zeros(total_neurons)
        # Here I choose what the connections are 
        # There Could be 4 options,
        #  - All connected
        #  - None connected and let it evolve
        #  - Random connections but enough to ensure input to output path
        #  - Random connections but without ensurance of input to output path


