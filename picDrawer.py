import seaborn as srn
import matplotlib.pyplot as plt
import pandas as pd

class PicDrawer(object):
   
    '''
	implemented by Li Jiaheng

	function :
		
		__init__

		get_corr_map : get heatmap of the correlatioin matrix
			input : none
			output : picture

		get_validation_comparison: get the comparison picture of prediction result and original result
			input : none
			output : picture
    '''

 
    def __init__(self, corr_matrix, pred_result, original_label):
	self.corr_matrix = corr_matrix
	self.pred = pred_result
	self.original = original_label

    def get_corr_map(self):
        srn.heatmap(self.corr_matrix)
	plt.show()

    def get_validation_comparison(self):
	plt.plot(self.pred, label="prediction")
	plt.plot(self.original.tolist(), label="validation")
	plt.legend()
	plt.show()
