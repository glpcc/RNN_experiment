import numpy as np
import math

class Network:
    def __init__(self, num_inputs, num_outputs, num_network_neurons, connection_type: str = 'ensure_connection', symetric_neuron_connections: bool = True, connection_probability: float = 0.6):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.num_network_neurons = num_network_neurons
        # Make just a local variable if not needed
        self.num_total_neurons = num_inputs + num_network_neurons + num_outputs
        self.neuron_values = np.zeros(self.num_total_neurons)
        self.activated_neurons = np.zeros(self.num_total_neurons)

        neuron_connections_options = ['full', 'empty', 'ensure_connection', 'random_connections']
        match connection_type:
            case 'full':
                self.neuron_connections = np.ones((self.num_total_neurons, self.num_total_neurons))
                np.fill_diagonal(self.neuron_connections,0)
            case 'empty':
                # no initial connections
                self.neuron_connections = np.zeros((self.num_total_neurons, self.num_total_neurons))
            case 'ensure_connection':
                # Random connections but enough to ensure input to output path 
                # (the graph of neurons must be connected)
                needed_conections = math.comb(self.num_total_neurons, 2)
                self.neuron_connections = np.array([0]*(self.num_total_neurons*self.num_total_neurons - needed_conections) + [1]*(needed_conections))
                rng = np.random.default_rng()
                rng.shuffle(self.neuron_connections)
                self.neuron_connections = np.reshape(self.neuron_connections, (self.num_total_neurons,self.num_total_neurons))
                if symetric_neuron_connections:
                    self.neuron_connections = np.maximum(self.neuron_connections,self.neuron_connections.T)
                np.fill_diagonal(self.neuron_connections,0)
            case 'random_connections':
                rnd = np.random.default_rng()
                self.neuron_connections = rnd.choice(
                    [0, 1], (self.num_total_neurons, self.num_total_neurons), p=[1-connection_probability, connection_probability])
                np.fill_diagonal(self.neuron_connections,0)
                if symetric_neuron_connections:
                    self.neuron_connections = np.maximum(self.neuron_connections,self.neuron_connections.T)
            case _:
                print(f'The connection type given ({connection_type}) isnt allowed try with one of these \n {neuron_connections_options}')

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
        # Implement some kind of activation function like tanh later if needed
        self.activated_neurons = np.where(self.neuron_values>self.neuron_thresholds,1,0)

        return self.neuron_values[len(self.neuron_values)-self.num_outputs:len(self.neuron_values)]


    def mutate(self,
    default_mutation_prob: float = 0.1,
    default_mutation_amount: float = 0.1,
    threshold_mutation_prob: None | float = None,
    weight_mutation_prob: None | float = None,
    bias_mutation_prob : None | float = None,
    connection_creation_mutation_prob: None | float = None,
    connection_removal_mutation_prob: None | float = None,
    threshold_mutation_amount: None | float = None,
    weight_mutation_amount: None | float = None,
    bias_mutation_amount: None | float = None,
    ):
        # Check for defaults
        if threshold_mutation_prob is None:
            threshold_mutation_prob = default_mutation_prob
        if weight_mutation_prob is None:
            weight_mutation_prob = default_mutation_prob
        if bias_mutation_prob is None:
            bias_mutation_prob = default_mutation_prob
        if connection_creation_mutation_prob is None:
            connection_creation_mutation_prob = default_mutation_prob
        if connection_removal_mutation_prob is None:
            connection_removal_mutation_prob = default_mutation_prob
        if threshold_mutation_amount is None:
            threshold_mutation_amount = default_mutation_amount
        if weight_mutation_amount is None:
            weight_mutation_amount = default_mutation_amount
        if bias_mutation_amount is None:
            bias_mutation_amount = default_mutation_amount

        # The mutations for the float values will be performed like this:
        # A neuron is selected for mutation based on the parameter probability of mutation 
        # and then the mutation amount will follow a normal distribution centered in 0 and 
        # with a standar deviation equal to the parameter mutation amount

        # Mutate the thresholds
        rng = np.random.default_rng()
        mutation_matrix = rng.choice([0,1], self.num_total_neurons, p = [1-threshold_mutation_prob,threshold_mutation_prob]) 
        self.neuron_thresholds += mutation_matrix*rng.normal(0,threshold_mutation_amount,self.num_total_neurons)
        
        # Mutate the weights
        mutation_matrix = rng.choice([0,1], (self.num_total_neurons,self.num_total_neurons), p = [1-weight_mutation_prob,weight_mutation_prob]) 
        self.connections_weights += mutation_matrix*rng.normal(0,weight_mutation_amount,(self.num_total_neurons,self.num_total_neurons))
    
        # Mutate the biases
        mutation_matrix = rng.choice([0,1], self.num_total_neurons, p = [1-bias_mutation_prob,bias_mutation_prob]) 
        self.neurons_biases += mutation_matrix*rng.normal(0,bias_mutation_amount,self.num_total_neurons)
    
        # Create new connections
        mutation_matrix = rng.choice([0,1], (self.num_total_neurons,self.num_total_neurons), p = [1-connection_creation_mutation_prob,connection_creation_mutation_prob]) 
        self.neuron_connections -= (self.neuron_connections-1)*mutation_matrix

        # Delete some connections
        mutation_matrix = rng.choice([0,1], (self.num_total_neurons,self.num_total_neurons), p = [1-connection_removal_mutation_prob,connection_removal_mutation_prob]) 
        self.neuron_connections -= self.neuron_connections*mutation_matrix
 


        