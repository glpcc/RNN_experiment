# Recurrent Neural Network Experiments
## Introduction
This is a repo in which I would experiment with a brain like recurrent neural network.
## Concept Explanation
Each neuron will be connected to a bunch of others including the input neurons that will activate every cycle with the desired input values and some output neurons that if activated will be the way to interact with the enviroment.
## Network Learning
Taking into account the difficulty that it would be to use backpropagation in this type of network, it would basicly evolve natural selection, i.e, mutations and survival of the fittest
## Algorithm (temporary basic explanation)
Every cycle the following will occur
```python
for input_neuron in network.input_neurons:
    input_neuron.activated = True
    input_neuron.value = input_value

for neuron in network.neurons:
    if neuron.activated:
        for conected_neuron in neuron.conected_neurons:
            concected_neuron.value += neuron.value * connection.weight

for neuron in network.neurons:
    if neuron.value >= neuron.activation_threshold:
        neuron.activated = True

for output_neuron in network.output_neurons:
    if output_neuron.value >= output_neuron.activation_value:
        output_neuron.make_action()
```
 
## First Experiment
After making the basics of the network class I would try it to make a small 2d car drive on its own in a little circuit.