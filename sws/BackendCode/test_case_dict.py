#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 17:41:34 2017

@author: zhihuixie
"""
import pandas as pd
import pickle as pl

def test_cases(df):
    '''
    this function makes a test case dict
    '''
    test_dict = {}
    keys = range(1, df.shape[0] + 1)
    values_info = df['HISTORY INFO'].values
    labels_info = df['STROKE_LABEL'].values
    for i in range(len(keys)):
        test_dict[str(keys[i])] = (values_info[i], labels_info[i])
    return test_dict

if __name__ == '__main__':    
    # read data into pandas dataframe
    df = pd.read_csv('../DataSet/stroke_his_info_db.csv')
    # convert data into dictionary
    test_dict = test_cases(df)
    print test_dict['4']
    # save data to local
    pl.dump(test_dict, open('../DataSet/test_dict.pkl', 'wb'))
    print 'Test cased written'