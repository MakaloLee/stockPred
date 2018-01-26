import numpy as np
import pandas as pd
import os


class CleanData(object):

    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists('../data/'):
            os.mkdir('../data')
        self.write_path = '../data'

    def clean_single_data(self, file_path):
        code_data = pd.read_csv(file_path)
        if not code_data.empty:
            time_split = pd.DataFrame((x.split(' ') for x in code_data.date), columns=['day', 'time'])
            code_data = code_data.drop(['date'], axis=1)
            code_data = pd.concat([time_split, code_data], axis=1)
            try:
                code_begin_pos = file_path.rfind('/')
                code_data.to_csv(os.path.join(self.write_path+file_path[code_begin_pos:]))
            except AttributeError:
                pass

    def get_file_list(self, file_dir):
        # acquire all complete .csv file path under a file director
        file_list = []
        for root, dirs, files in os.walk(file_dir):
            for f in files:
                if os.path.splitext(f)[1] == '.csv':
                    file_list.append(os.path.join(root, f))
        return file_list

    def run(self):
        file_path_list = self.get_file_list(self.file_path)
        for file_path in file_path_list:
            self.clean_single_data(file_path)

