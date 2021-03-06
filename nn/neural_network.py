import random
import numpy as np

from nn.transfer import DERIVATIVE, FUNCTION, TRANSFER_FUNCTIONS

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
            weights = [float(weight) for weight in self.weights],
            bias = self.bias,
            transfer = self.transfer_fx_name
        )

class ArtificialNeuralNetwork:

    input_layer = None
    layers = None
    learning_rate = 0.1

    def __init__(self):
        raise NotImplementedError("This is an abstract class and must be inherited!")

    def set_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate

    def forward(self, inputs):
        """
        Forwards the inputs, where inputs is a row in a dataset,
        through the neurons in each layer and returns the output layer
        outputs.
        """
        for layer in self.layers:
            outputs = []
            for neuron in layer:
                output = neuron.forward(inputs)
                neuron.output = output
                outputs.append(output)
            inputs = outputs # set the inputs to the outputs of the layer
        return inputs

    def train(self, *args):
        raise NotImplementedError()

    def train_without_update(self, *args):
        raise NotImplementedError()

    def apply_weight_gradients(self, *args):
        raise NotImplementedError()

    def json(self):
        """
        Serializes the model into a JSON formatted object
        :return:
        """
        json_network = {
            "output": [neuron.json() for neuron in self.layers[-1]],
            "hidden": []
        }

        if len(self.layers) > 1:
            json_network["hidden"] = [[neuron.json() for neuron in layer] for layer in self.layers[:-1]]
        
        return json_network