# -*- coding: utf-8 -*-
"""
this class transforms data, selects features and trains machine learning model
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
import re
import pickle as pl
import numpy as np
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import LinearSVC
from nltk.stem.snowball import SnowballStemmer


class RiskPredictor():
    '''
    this class transforms data, selects features and trains machine learning model
    load_data - load csv file into pandas dataframe
    tokenizer - applu stemmer to text
    transform_X - transform text features based on tfidf
    transform_y - tranform y label into numberic value
    feature_selection - apply lasso to do feature selection
    model_selection - search optimized parameters for model
    train_clf - train a machine learning model
    '''
    def __init__(self, path):
        '''
        set up variables, take file path as a parameter
        '''
        # file path
        self.path = path
        # pandas data frame
        self.data_frame = None
        # features
        self.X = None
        # numeric target
        self.y = None
        # feature selection model
        self.model = None
        # tfidf vectorizer
        self.vec = None
        # labels
        self.labels = None
        # training model
        self.clf = None
        # transformed features
        self.X_transform_tfidf = None
        # positive relevant stroke factors
        self.risk_factors = None
        # negative relevant stroke factors
        self.anti_risk_factors = None
        
    def load_data(self):
        '''
        load a file from path to pandas dataframe
        '''
        self.data_frame = pd.read_csv(self.path)
        print 'Data loaded.\n'
        
    def tokenizer(self, s):
        '''
        apply stem to each input text
        '''
        # set up a stemmer
        stemmer = SnowballStemmer('english')
        stemmed = []
        # remove special characters
        s = re.sub('[^a-zA-Z0-9]+', ' ', s)
        s = re.sub('[ ]+', ' ', s)
        s.strip()
        # split text into a list of words
        words = s.split()
        # apply stemming to each word
        for item in words:
            stemmed.append(stemmer.stem(item))  
        # return the stemmed word
        return ' '.join(stemmed)   
        
    def transform_X(self):
        '''
        use tfidf to transform text into weighted word occurance
        '''
        # set up a vector
        tfidf_vec = TfidfVectorizer(ngram_range = (2,2), stop_words = 'english')
        # get text values
        X = self.data_frame['HISTORY INFO'].values
        # apply stemmer to each text input
        X = [self.tokenizer(s) for s in X]
        # apply transformation
        self.X_transform_tfidf = tfidf_vec.fit_transform(X)
        self.vec = tfidf_vec
        print 'Features are transformed.\n'
    
    def transform_y(self):
        '''
        transform labels into numberic values
        '''
        # get label values
        labels = self.data_frame['STROKE_LABEL'].values
        # make a dictionary for labels, Non-stroke: 0, stroke: 1
        labels_dict = {'Non-Stroke': 0, 'Stroke':1}
        # transform labels
        self.y = [labels_dict[key] for key in labels]
        self.labels = labels_dict
        print 'Labels are transformed.\n'
        
    def feature_selection(self, clf_feature_selection):
        '''
        this function performs feature selection
        '''
        # train a model for feature selection 
        clf_feature_selection.fit(self.X_transform_tfidf, self.y)
        self.model = SelectFromModel(clf_feature_selection, prefit=False)
        # get selected new features
        self.X = self.model.fit_transform(self.X_transform_tfidf, self.y)
        # get coefficient for features
        coef = clf_feature_selection.coef_[0]
        # sort index based on coefficient values
        indices = np.argsort(coef)[::-1]
        # get features and their coefficients which are greater than 0.1
        indices_positive = [i for i in indices if coef[i] > 0.1]
        weights = [coef[i] for i in indices_positive]
        feature_names = self.vec.get_feature_names()
        positive_terms = [str(feature_names[i]) for i in indices_positive]
        # get features and their coefficients which are smaller than -0.1
        indices_negative = [i for i in indices if coef[i] < -0.1]
        negative_terms = [str(feature_names[i]) for i in indices_negative]
        # assign risk factors and anti_risk_factors 
        self.risk_factors = zip(positive_terms, weights)
        self.anti_risk_factors = negative_terms
        
    def model_selection(self, parameters, clf = LogisticRegression(random_state = 42)):
        '''
        this method searchs the best parameters for a model
        '''
        model = GridSearchCV(clf, parameters, cv = 5, n_jobs =1, 
                             scoring = 'recall_macro')
        model.fit(self.X, self.y)
        best_parameter = model.best_params_
        print 'Best parameters for tfidf vectorizer (LogisticRegression): ', best_parameter
        return best_parameter
        
    def train_clf(self, clf):
        '''
        train the model based on the optimized parameters
        '''
        #partial_fit
        clf.fit(self.X, self.y)
        self.clf = clf
        print 'Model is trained.\n'
    
if __name__ == '__main__':
    '''
    feature selection and train models
    '''
    # load data
    path = '../DataSet/stroke_his_info.csv'
    dp = RiskPredictor(path)
    dp.load_data()
    # data transformation
    dp.transform_X()
    dp.transform_y()
    
    # select features
    lsvc = LinearSVC(C = 0.5, penalty='l1', dual = False, random_state = 42)
    dp.feature_selection(lsvc)
    
    # perform model selection
    lr_parameters = {'tol' : np.logspace(-7, -3, 5),
                     'C' : np.logspace(-3, 3, 6),
                     'penalty' : ['l1', 'l2']} 
    params = dp.model_selection(lr_parameters)
    clf = LogisticRegression(random_state = 42, **params)
    dp.train_clf(clf)
    # get trained model, selected model, labels, risk factors and anti-risk factors
    clf = dp.clf
    model = dp.model
    vec = dp.vec
    labels = dp.labels
    risk_factors = dp.risk_factors
    anti_risk_factors = dp.anti_risk_factors
    # print out risk factors
    print risk_factors
    # pick up risk factors based on domain knowledge
    risk_factors = [('stroke seizur', 'stroke seizure', 4.7675728927962036), 
                    ('stroke age', 'stroke age', 3.2344982042974415), 
                    ('atrial fibril', 'atrial fibrillation', 3.0761705519408156), 
                    ('prior stroke', 'prior stroke', 2.8609798596656395), 
                    ('mother stroke', 'mother stroke', 2.8380363841598819), 
                    ('intracerebr hemorrhag', 'intracerebral hemorrhage',2.7507977472828307), 
                    ('histori aneurysm', 'aneurysm', 2.6845018357096326), 
                    ('afib coumadin', 'atrial fibrillation and coumadin' ,2.5636135513259224), 
                    ('subarachnoid hemorrhag', 'subarachnoid hemorrhage', 2.5041963819931441), 
                    ('pneumocysti carinii', 'pneumocystis carinii', 2.3369816889560062), 
                    ('hypertens stroke', 'hypertension', 2.2972148918716897), 
                    ('high cholesterol', 'high cholesterol', 2.2883344396052574), 
                    ('mucin cystadenoma', 'mucin cystadenoma', 2.2536536122421955), 
                    ('neurolog diseas', 'neurological disease', 2.2510422035943662), 
                    ('mellitus dermatomyos', 'mellitus dermatomes', 2.180390626655782), 
                    ('earli stroke', 'early stroke', 2.072916995102652), 
                    ('histori stroke', 'history stroke', 2.0519828875553339), 
                    ('hypertens medic', 'hypertens medical condition', 1.7223762136050498), 
                    ('brother stroke', 'brother stroke', 1.6898895148058837), 
                    ('acetylsalicyl acid', 'acetylsalicyl acid', 1.6607789000782713), 
                    ('stroke famili', 'stroke family', 1.6312797014572826), 
                    ('hemorrhag stroke', 'hemorrhage', 1.6059352765935688), 
                    ('cerebr aneurysm', 'cerebral aneurysm', 1.4401028953210531), 
                    ('hypertens afib', 'hypertension and atrial fibrillation', 1.3222012095458102), 
                    ('etoh drug', 'alcohol and drug',1.2405474009354533), 
                    ('cardiac stent', 'cardiac sentation', 1.2142891454962819), 
                    ('tob etoh', 'tobacco and alcohol', 1.1424776733390074), 
                    ('hypertens breast', 'hypertens breast',1.134856271913228), 
                    ('social etoh', 'social alcohol', 1.0955932784986355), 
                    ('stroke father', 'stroke father',1.0740204851727311), 
                    ('ischem attack', 'ischemic attack', 1.0526057440894012), 
                    ('hypertens live', 'hypertension live', 0.94005970413092266), 
                    ('hypertens year', 'hypertension year', 0.91395355087859442), 
                    ('brain aneurysm', 'brain aneurysm', 0.82480800044851121), 
                    ('macular degener', 'macular degeneration', 0.8113539655158043), 
                    ('hyperlipidemia coronari', 'hyperlipidemia coronary', 0.7879653453794111), 
                    ('hypertens hyperlipidemia', 'hypertension and hyperlipidemia', 0.70433447302375984), 
                    ('father stroke', 'father stroke', 0.66624596635709554), 
                    ('hypertens hepat', 'hypertension and hepat', 0.6521671980344167), 
                    ('borderlin diabet', 'borderlin diabetes', 0.64823464401327924), 
                    ('fib coumadin', 'fibrillation and coumadin', 0.61972263550839535), 
                    ('dermatomyos hypertens', 'dermatomes hypertension', 0.55497425122508814), 
                    ('mother tobacco', 'mother tobacco', 0.50566380928845611),
                    ('hypertens diabet', 'hypertension diabete', 0.46602539889117284), 
                    ('intracrani hemorrhag', ' intracranial hemorrhage', 0.46440172710485222), 
                    ('ago hypertens', 'ago hypertension', 0.44087240016875456), 
                    ('brain tumor', 'brain tumor', 0.43609319327271334), 
                    ('stroke myocardi', 'stroke myocardial', 0.38560910351534239), 
                    ('diseas myocardi', 'disease myocardial', 0.33991659569978938), 
                    ('current smoker', 'current smoker', 0.18863336477311962), 
                    ('surgeri hypertens', 'surgery and hypertension', 0.17320639218321501), 
                    ('memori problem', 'memory problem', 0.17277096674702574), 
                    ('hypertens high', 'hypertension high', 0.16935870942431358), 
                    ('nitric oxid', 'nitric oxid', 0.16086330785188319), 
                    ('smoke drink', 'smoke drink', 0.15205139796099434), 
                    ]
    # save files
    pl.dump(clf, open('../DataSet/clf_lr.pkl', 'wb'))
    pl.dump(labels, open('../DataSet/labels.pkl', 'wb'))
    pl.dump(vec, open('../DataSet/vec.pkl', 'wb'))
    pl.dump(model, open('../DataSet/model.pkl', 'wb'))
    pl.dump(risk_factors, open('../DataSet/risk_factor.pkl', 'wb'))
    pl.dump(anti_risk_factors, open('../DataSet/anti_risk_factor.pkl', 'wb'))
  
    print 'Data are saved successfully!'
    