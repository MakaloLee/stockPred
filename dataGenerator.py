import pandas as pd
import numpy as np
from sklearn import preprocessing
from util import *

class DataGenerator(object):
    
    '''

	implemented by Li Jiaheng

	function :
		
		__init__

		get_code_data_set: get all the data
			input : stock code
			output : a panel storing all data we need	

		train_test_split: split dataset
			input : none
			output :  train set, train label, test set, test label

    '''


    def __init__(self, file_path, code, test_set_ratio, corr, train_set_choice):
        self.file_path = file_path
        self.code = code
        self.test_set_ratio = test_set_ratio
        self.file_list = get_file_list(file_path)
        self.stocks_data_dict = load_all_data(self.file_list)
        self.corr = corr
        self.stock_panel = None
	if train_set_choice == 1:
	    self.train_set_choice = 1.0
	else:
	    self.train_set_choice = 0.2

    def get_code_data_set(self, code, ahead_num=11):
        correlated_stock = pd.DataFrame(self.corr[code].values, index=self.corr.columns, columns=[code])
        # get the stocks with strong correlation
	correlated_stock = correlated_stock[abs(correlated_stock) >= self.train_set_choice].dropna()
        for key, value in self.stocks_data_dict.items():
	    if key not in correlated_stock.index:
                continue
            hour = []
	    time_split = value['time'].tolist()
            for split in range(len(time_split)):
		time_split[split] = time_split[split].split(':')
		time_split[split] = map(int, time_split[split])
            for time in time_split:
	        if time[0] >= 9 and time[0] <= 11:  #one-hot encoding
                    hour.append([0, 1])
                else:
                    hour.append([1, 0])
	    features = value.loc[:, ['p_change']].astype(np.float64)
            used_features = pd.concat([pd.DataFrame(hour), pd.DataFrame(features)], axis=1)
	    # used_features.loc[:, ['open']] = preprocessing.scale(used_features.loc[:, ['open']])
	    used_features.loc[:, ['p_change']] = used_features.loc[:, ['p_change']] * self.corr[code][key]
	    self.stocks_data_dict[key] = used_features

        used_stocks_panel = {}
        for stocks in correlated_stock.index:
	    if stocks in self.stocks_data_dict.keys():
		used_stocks_panel[stocks] = self.stocks_data_dict[stocks].dropna(axis=0)

        self.stock_panel = pd.Panel(used_stocks_panel)

    def train_test_split(self):
        all_data_frame = []
	test = []
        # extract all dataframes
        for item, value in self.stock_panel.iteritems():
	    if str(item) == self.code:
		test = value.iloc[int(value.shape[0] * self.test_set_ratio)+1:, :].dropna(axis=0).astype(np.float64)
		value = value.iloc[:int(value.shape[0] * self.test_set_ratio), :]
            else:
		value = value.iloc[:int(value.shape[0] * self.test_set_ratio), :]
	    all_data_frame = pd.concat([pd.DataFrame(all_data_frame), value.dropna(axis=0)], axis=0)
	length = all_data_frame.shape[0]
	train = all_data_frame.astype(np.float64)
        train_feature = train.drop(['p_change'], axis=1)
        train_label = train.loc[:, 'p_change']
        test_feature = test.drop(['p_change'], axis=1)
        test_label = test.loc[:, 'p_change']
        return train_feature, train_label, test_feature, test_label

    def run(self):
        self.get_code_data_set(self.code)
        train_feature, train_label, test_feature, test_label = self.train_test_split()

        return train_feature, train_label, test_feature, test_label

