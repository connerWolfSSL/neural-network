import json, random
import numpy as np

from transfer import DERIVATIVE, FUNCTION, TRANSFER_FUNCTIONS

class Neuron:

    delta = None
    output = None

    def __init__(self, num_inputs = None, transfer_function = "logistic",
                neuron_json = None):
        if neuron_json is None:
            self.weights = np.random.rand(num_inputs)
            self.bias = random.random()
        else:
            self.weights = neuron_json["weights"]
            self.bias = neuron_json["bias"]
            transfer_function = neuron_json["transfer"]
        if not transfer_function in TRANSFER_FUNCTIONS:
            raise "Invalid transfer function %s" % transfer_function
        self.transfer_fx = TRANSFER_FUNCTIONS[transfer_function]
        self.transfer_fx_name = transfer_function

    def forward(self, inputs):
        return self.transfer(self.activate(inputs))

    def activate(self, inputs):
        return np.dot(self.weights, inputs) + self.bias

    def transfer(self, activation):
        return self.transfer_fx[FUNCTION](activation)

    def transfer_derivative(self, value):
        """
        Logistic function derivative
        """
        return self.transfer_fx[DERIVATIVE](value)

    def json(self):
        return dict(
            weights = self.weights,
            bias = self.bias,
            transfer = self.transfer_fx_name
        )

class ArtificialNeuralNetwork:

    input_layer = None
    layers = None

    def __init__(self):
        raise NotImplementedError("This is an abstract class and must be inherited!")

    def forward(self, inputs):
        inputs = [node.forward(inputs) for node in self.input_layer]
        for layer in self.layers:
            new_inputs = []
            for neuron in layer:
                output = neuron.forward(inputs)
                neuron.output = output
                new_inputs.append(output)
            inputs = new_inputs
        return inputs

    def json(self):
        json_network = {
            "input": [neuron.json() for neuron in self.input_layer],
            "output": [neuron.json() for neuron in self.layers[-1]],
        }

        if len(self.layers) > 1:
            json_network["hidden"] = [[neuron.json() for neuron in layer] for layer in self.layers[:-1]]
        
        return json_network