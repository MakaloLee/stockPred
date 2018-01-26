from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression

class Regression(object):

    '''
	implemented by Li Jiaheng


	functions:
		
		__init__
		
		fit : used for training model

		predict : used for prediction

		score : used for validation

	input: method, train data, train label. test data, test label

	output: predict lavel, score

    '''


    def __init__(self, method):
	self.regressor = None
	self.method = method

    def fit(self, train_data, train_label):
        if self.method == "NeuralNetwork":
	    regressor = MLPRegressor(solver='adam', hidden_layer_sizes=(1, 20), random_state=5)
 	elif self.method == "LinearRegression":
	    regressor = LinearRegression(normalize=False)
	regressor.fit(train_data, train_label)
	self.regressor = regressor

    def predict(self, test_data):
        pred_label = self.regressor.predict(test_data).tolist()
        return pred_label

    def score(self, test_label, test_set):
        loss = self.regressor.score(test_set, test_label)
        return loss
