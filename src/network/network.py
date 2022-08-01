import numpy as np
import math

class Network:
    def __init__(self, num_inputs, num_outputs, num_network_neurons):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.num_network_neurons = num_network_neurons
        # Make just a local variable if not needed
        self.num_total_neurons = num_inputs + num_network_neurons + num_outputs
        self.neuron_values = np.zeros(self.num_total_neurons)
        self.activated_neurons = np.zeros(self.num_total_neurons)

        # Here I choose what the connections are
        # There Could be 4 options,
        #  - All connected
        # self.neuron_connections = np.ones((self.num_total_neurons, self.num_total_neurons))
        # np.fill_diagonal(self.neuron_connections,0)
        
        #  - None connected and let it evolve
        # self.neuron_connections = np.zeros((self.num_total_neurons, self.num_total_neurons))
        
        #  - Random connections but enough to ensure input to output path (the graph of neurons must be connected)
        #    conecctions are symetric to ensure connections
        # needed_conections = math.comb(self.num_total_neurons, 2)
        # self.neuron_connections = np.array([0]*(self.num_total_neurons*self.num_total_neurons - needed_conections) + [1]*(needed_conections))
        # rng = np.random.default_rng()
        # rng.shuffle(self.neuron_connections)
        # self.neuron_connections = np.reshape(self.neuron_connections, (self.num_total_neurons,self.num_total_neurons))
        # self.neuron_connections = np.maximum(self.neuron_connections,self.neuron_connections.T)
        # np.fill_diagonal(self.neuron_connections,0)

        #  - Random connections but without ensurance of input to output path
        rnd = np.random.default_rng()
        self.neuron_connections = rnd.choice(
            [0, 1], (self.num_total_neurons, self.num_total_neurons), p=[0.4, 0.6])
        np.fill_diagonal(self.neuron_connections,0)
        # With symetricc conecctions
        # self.neuron_connections = np.maximum(self.neuron_connections,self.neuron_connections.T)

        # Initialize the weights of the connections and the biases of the neurons
        rnd = np.random.default_rng()
        self.connections_weights = rnd.random((self.num_total_neurons,self.num_total_neurons))
        self.neurons_biases = np.zeros(self.num_total_neurons)
    
        # Initialize the thresholds for neuron activation
        self.neuron_thresholds = rnd.random(self.num_total_neurons)*10
    
    def run_step(self,inputs):
        if len(inputs) == self.num_inputs:
            self.neuron_values[0:self.num_inputs] = np.array(inputs)
            self.activated_neurons[0:self.num_inputs] = np.ones(self.num_inputs)
        else:
            print(f'Incorrect amount of inputs {len(inputs)} where given but {self.num_inputs} are needed')
        
        # Here I calculate the neuron values as stated in the readme pseudo code
        self.neuron_values = np.sum(((self.activated_neurons*(self.neuron_values+self.neurons_biases))*self.neuron_connections)*self.connections_weights,axis=1)