import os
import pandas as pd

class CalcCorrMatrix(object):

    '''

	implemented by Li Jiaheng

	functions:

		__init__

		run : calculate correlation
			input : none
			output : correlation matrix

		readfiles : read files from ../data/
			input : none
			output : a dictionary of all stocks' data

		del_empty_frame : delete empty dataframe
			input : a dictionary of all stocks' data
			output : a dictionar of all stocks' data

    '''

    def __init__(self):
        self.file_path = "../data/"
	self.file_list = []

    def run(self):
        corr_pairs = []
        stock_dict = self.readfiles()

        stock_dict = self.del_empty_frame(stock_dict)

        # calculate correlations, return the correlations of stock_code
        key_feature = ['p_change']
        for key_iter in range(len(key_feature)):
            compare = []
            for key, value in stock_dict.items():
		compare.append(value[key_feature[key_iter]].tolist())
            compare_frame = pd.DataFrame(compare)
            compare_frame = compare_frame.transpose()
            corr = pd.DataFrame(compare_frame.corr().values, index=self.file_list, columns=self.file_list)
	return corr

    def readfiles(self):
        path = os.walk(self.file_path)
        root = ""
        files = []
        for root_path, dirs, contained_files in path:
            root = root_path
            files = contained_files
	
        stock_dict = {}
        for one_file in files:
            stock_data = pd.read_csv(root + '/' + one_file)
            if stock_data.empty:
                continue
            stock_code = one_file.split('.')[0]
	    self.file_list.append(stock_code)
            date = stock_data['time']
            stock_data = stock_data.drop(['time'], axis=1)
	    column = stock_data.columns
	    panel_index = stock_dict.keys()
            stock_data = pd.DataFrame(stock_data.values, index=date, columns=column)
	    stock_data = stock_data.drop([stock_data.columns[0]], axis=1)
            stock_dict[stock_code] = stock_data

        return stock_dict

    def del_empty_frame(self, stock_dict):
        for item, value in stock_dict.iteritems():
            stock_frame = stock_dict[item]
            stock_frame = stock_frame.dropna(axis=1, how='all')
            if len(stock_frame.columns) == 0:
                stock_dict = stock_dict.drop([item], axis=0)

        return stock_dict
