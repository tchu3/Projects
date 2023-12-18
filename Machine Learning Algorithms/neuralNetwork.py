import numpy as np
import matplotlib.pyplot as plt

# Define the sigmoid function
def sigmoid(x):
  return 1/(1+np.exp(-x))

# Define the derivative function
def sigmoidDerivative(x):
    # does not include sigmoid functions in this derivative because the arguments being passed have already been 'activated'
  return x*(1-x)

class Layer:
    def __init__(self, inputs, neurons, weights=None, bias=None):
        self.weights = weights if weights is not None else np.random.rand(inputs, neurons)
        self.bias = bias if bias is not None else np.random.rand(neurons)
        self.activation = None
        # error is the error of a specific layer
        self.error = None
        # delta is the error applied to a specific layer
        self.delta = None
    
    def activate(self, inputs):
        # Take the dot product of the weights and the input layer plus the bias (Wx + bias)
        #print (inputs)
        #print (self.weights)
        #print (self.bias)
        activationStep = np.dot(inputs, self.weights) + self.bias
        # Apply the activation function to the linear function
        activationStep = sigmoid(activationStep)
        self.activation = activationStep
        
        return self.activation
        
class tcNeuralNetwork:
    # Initializing the neutral network
    def __init__(self):
        self._layers = []
        
    def addLayer(self, layer):
        self._layers.append(layer)
        
        '''
        # Defining the input array
        self.input = x
        # Defining number of nodes in hidden layer
        self.nodes = z
        
        # Defining 3 hidden layers
        # Defining the first layer of weights as the same size of the inputs | shape[1] = columns = 1  |  shape[0] = rows
        self.weights1 = np.random.rand(self.input.shape[1],z) 
        self.weights2 = np.random.rand(z,z)
        self.weights3 = np.random.rand(z,1)
        # Defining the ACTUAL output array from the data (training data)
        self.y = y
        # Defining the CALCULATED output array
        self.output = np.zeros(y.shape)
        '''

    def feedForward(self, x):
        # For each layer activate each layer via weights + activation function
        for layer in self._layers:
            layerActivated = layer.activate(x)
            
        return layerActivated
    
        '''
        # HiddenLayer 1 is defined as the dot product of (weights)(input) + (bias)
        # Bias is equal to a 1 row and "z" columns - size of hidden layer
        self.layer1Bias = np.zeros((1,z))
        self.hiddenLayer1 = sigmoid(np.dot(self.input, self.weights1) + self.layer1Bias)
        
        # Layer 2  defined as the dot product of (weights)(input) + (bias)
        # Bias is equal to a 1 row and "z" columns - size of hidden layer
        self.layer2Bias = np.zeros((1,z))
        self.hiddenLayer2 = sigmoid(np.dot(self.hiddenLayer1, self.weights2) + self.layer2Bias)
        
        # Defining the output layer as the dot product of the (weights)(output layer 1) + (bias)
        # Bias is equal to a 1 row and "z" columns - size of hidden layer
        # Output layer - Regression = linear function | Classification = softmax fucntion or sigmoid
        self.layer3Bias = np.zeros((1,z))
        self.output = sigmoid(np.dot(self.hiddenLayer2, self.weights3) + self.layer3Bias)
        return self.output
        '''
        
    def backPropagation(self, x, y, learningRate):
        # where x is the input values for a specific layer
        # where y is the output values for a specific layer
        
        # For iteration the outputs are equal to result of the feed forward step
        outputs = self.feedForward(x)
        
        # Loop over the layers from the end to back propagate the error i.e. 3 layers = [2,1,0]
        for i in reversed(range(len(self._layers))):
            layer = self._layers[i]
            
            # Check if this is the output layer | -1 refers to the last element i.e. 0 
            if layer == self._layers[-1]:
                # derivative of the loss function = 1/2*(y-output)^2 *derivative of linear function wrt to Weights
                layer.error = (y - outputs)
                layer.delta = layer.error * sigmoidDerivative(outputs)
            else:
                # Next layer is ACTUALLY the previous layer in the neural network
                nextLayer = self._layers[i+1]
                # Next layer is actually the layer we just previously computed
                layer.error = np.dot(nextLayer.weights, nextLayer.delta)
                # sigmoidDerivative can be multiplied because it is simply a scalar vector
                layer.delta = layer.error * sigmoidDerivative(layer.activation)
                print(layer.activation)
                print (sigmoidDerivative(layer.activation))
        
        # Updating the weights
        for i in range(len(self._layers)):
            layer = self._layers[i]
            # Shape the inputs into a 2d array of rows 1, '# attributes' columns
            # When you're at the first hidden, set inputs to the input column
            # Otherwise set the input layer to the previous hidden layer post activation
            currentInputs = np.atleast_2d(x if i == 0 else self._layers[i-1].activation)
            layer.weights += layer.delta * currentInputs.T * learningRate
            layer.bias += layer.delta * learningRate
        '''
        # Caculating the error associated with the output
        # Error is calculated as the derivative of the loss function (y-ybar)^2 with respect to weights 3
        # Uses multiplication to apply the error not dot product
        tempError = 2*(self.y-self.output)*sigmoidDerivative(self.output)
        errorWeights3 = np.dot(self.hiddenLayer2.T,tempError)
        
        # Error is calculated as the derivative of the loss function (y-ybar)^2 with respect to weights 2
        tempError = np.dot(tempError, self.weights3.T)*sigmoidDerivative(self.hiddenLayer2)
        errorWeights2 = np.dot(self.hiddenLayer1.T, tempError)
            
    
        # Error is calculated as the derivative of the loss function (y-ybar)^2 with respect to weights 1
        tempError = np.dot(tempError, self.weights2.T)*sigmoidDerivative(self.hiddenLayer1)
        errorWeights1 = np.dot(tempError, self.input)
        
        # Update the weights according to the error above - no learning rate applied
        self.weights1 += errorWeights1
        self.weights2 += errorWeights2
        self.weights3 += errorWeights3
        return self.weights1
        '''
        
    def train(self, inputs, outputs, learningRate, maxCycles):
        
        meanSquareErrors = []
        
        for i in range(maxCycles):
            # Loops through each training example and performs back propagation
            for j in range (len(inputs)):
                self.backPropagation(inputs[j],outputs[j],learningRate)
            # Calculate mean square error every 10 trials
            
            if i % 10 == 0:
                currentError = np.mean(np.square(outputs - testNetwork.feedForward(inputs)))
                meanSquareErrors.append(currentError)
                print('Cycle: #%s, MSE: %f' % (i, float(currentError)))
        return meanSquareErrors
    
            
        '''
        # Set the output as the initial feed output calculated from feed forward
        self.output = self.feedForward()
        # Back propagate to reduce error
        self.backPropagation()
        '''

x=np.array(([0,0,1],[0,1,1],[1,0,1],[1,1,1]), dtype=float)
y=np.array(([0],[1],[1],[0]), dtype=float)

testNetwork = tcNeuralNetwork()
testNetwork.addLayer(Layer(3,3))
testNetwork.addLayer(Layer(3,3))
testNetwork.addLayer(Layer(3,1))

errors = testNetwork.train(x,y,0.3,500)
plt.plot(errors)


