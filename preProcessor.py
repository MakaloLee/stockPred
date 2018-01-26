from processor.calcCorrMatrix import CalcCorrMatrix
from processor.cleanData import CleanData
from dataGenerator import DataGenerator


class PreProcessor(object):

    '''
	implemented by Li Jiaheng

	this class is used for preprocessing data

	input: train set choice, stock code, file path ratio

	output: train set, train label, test set, lest label, correlation matrix
    '''


    def __init__(self, train_set_choice, code, file_path, ratio, preprocess):
	self.train_set_choice = train_set_choice
	self.code = code
	self.file_path = file_path
	self.ratio = ratio
	self.preprocess = preprocess

    def run(self):
	if self.preprocess == 1:
            print "cleaning data...\n"
	    clean_data = CleanData(self.file_path)
            clean_data.run()
	    print "cleaning data successfully\n"

	print "calculating correlation matrix...\n"
        calc_corr = CalcCorrMatrix()
        corr_matrix = calc_corr.run()
	print "calculatE successfully\n"

	print "generating dataset...\n"
        data_generator = DataGenerator('../data/', self.code, self.ratio, corr_matrix, self.train_set_choice)
        train_feature, train_label, test_feature, test_label = data_generator.run()
	print "generate successfully\n"

        return train_feature, train_label, test_feature, test_label, corr_matrix


