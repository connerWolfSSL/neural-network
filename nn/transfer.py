import numpy as np

FUNCTION = "function"
DERIVATIVE = "derivative"

def logistic(value):
    return 1 / (1 + np.exp(-value))

def logistic_deriv(value):
    return value * (1.0 - value)

def linear(value):
    return value

def linear_deriv(value):
    return 1

def tanh(value):
    return np.tanh(value)

def tanh_deriv(value):
    return 1 - value**2

TRANSFER_FUNCTIONS = {
    "logistic": {
        FUNCTION: logistic,
        DERIVATIVE: logistic_deriv
    },
    "linear": {
        FUNCTION: linear,
        DERIVATIVE: linear_deriv 
    },
    "tanh": {
        FUNCTION: tanh,
        DERIVATIVE: tanh_deriv
    }
}