from preProcessor import PreProcessor
import argparse
from regression import Regression
from picDrawer import PicDrawer


if __name__ == '__main__':

    '''
    
        python run filepath code  [-m] [-r] [-s] [-p]
    
    output:
        stock error : implement by regression.score() 
        picture : implement by drawer
    
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str, help="the directory of the .csv file")
    parser.add_argument("code", type=str, help="the stock code you want to predict")
    parser.add_argument("-m", "--method", type=str,
                        default='NeuralNetwork', help="the method used to do this task")
    parser.add_argument("-r", "--ratio", type=float,
                        default=0.2, help="the validate data set ratio")
    parser.add_argument("-s", "--train_set", type=float, default=1.0, help="the minimun correlation of stocks we use in train set, 1 means the train set doesn't includes other stocks")
    parser.add_argument("-p", "--preprocess", type=int, default=1,  help="preprocessing or not")
    args = parser.parse_args()

    file_path = args.filepath
    train_set_choice = args.train_set
    code = str(args.code)
    method = args.method

    # create pre processor
    data_cleaner = PreProcessor(train_set_choice, code, file_path, args.ratio, args.preprocess)
    train_feature, train_label, test_feature, test_label, corr = data_cleaner.run()
    print test_label
    reg = Regression(args.method)
    
    print "training model...\n"
    reg.fit(train_feature, train_label)
    print "predicting...\n"
    pred_result = reg.predict(test_feature)
    print "scoring...\n"
    score = reg.score(test_label, test_feature)

    print "drawing...\n"
    drawer = PicDrawer(corr, pred_result, test_label)
    drawer.get_corr_map()
    drawer.get_validation_comparison()

    print("score" + str(score))

    print "regressor exit!"


