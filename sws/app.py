#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 09:42:18 2017

@author: zhihuixie
"""
'''
import libraries for analysis
'''
from flask import Flask, render_template, request, url_for
import pickle as pl
import re
import os
from nltk.stem.snowball import SnowballStemmer


'''
This section define functions for the app
'''
def load_state():
    '''
    load trained classifier, saved labels, vectorizer, feature selection model
    and risk factors and test cases
    '''
    labels = pl.load(open('DataSet/labels.pkl', 'rb'))
    clf = pl.load(open('DataSet/clf_lr.pkl', 'rb'))
    t_vector = pl.load(open('DataSet/vec.pkl', 'rb'))
    model = pl.load(open('DataSet/model.pkl', 'rb'))
    risk_factors = pl.load(open('DataSet/risk_factor.pkl', 'rb'))
    test_dict = pl.load(open('DataSet/test_dict.pkl', 'rb'))
    return clf, t_vector, labels, model, risk_factors, test_dict

def clean_input (history_info):
    '''
    clean input text
    '''
    # set up a stemmer
    stemmer = SnowballStemmer('english')
    stemmed = []
    # remove special characters and blank spaces
    history_info = re.sub('\[.*?\]', '', history_info)
    non_special_chars = "[^a-zA-Z0-9]+"
    history_info = re.sub(non_special_chars, ' ', history_info)
    history_info = re.sub('[ ]+', ' ', history_info)
    # split words
    history_info.strip()
    words =  history_info.split()
    # apply stemmer to each word
    for word in words:
        stemmed.append(stemmer.stem(word))   
    return ' '.join(stemmed) 
    
def predict(history_info, clf, t_vector, labels, model):
    '''
    predict record using the trained classifier
    '''
    global feature
    # text feature transformation
    t_feature = t_vector.transform([clean_input(history_info)])
    feature = model.transform(t_feature)
    # predict probabilty 
    results_prob = clf.predict_proba(feature)
    # return predict results
    return t_feature, '%.2f'%(results_prob[0][1]*100)
    
# load states
global test_dict
clf, t_vector, labels, model, risk_factors, test_dict = load_state()


'''
This section is used to retrieve information from test cases, 
and add new information to test cases
'''
 
def database_query(test_dict, user_id):
    '''
    search test_dict and return the ID and HISTORY INFO that match the 
    user_id
    '''
    try:
        dict_result = test_dict[user_id]
        query_result = [dict_result[0]]
        query_id = [user_id]
    except KeyError:
        query_result, query_id = [], []
    return query_result, query_id
    
def database_update(test_dict, history_info, user_id):  
    '''
    update test cases with new history_info for user_id
    '''
    test_dict[user_id] = (history_info, 'Not labeled')
    
def database_length(dict_test):
    '''
    get number of users in the test cases
    '''
    return len(dict_test)

'''
The following code is applied to flask web framework and transfer data between 
frontend and backend
'''
app = Flask(__name__)


@app.route('/')
def index():
    '''
    flask webframe starting page
    '''
    return render_template('index.html')

@app.route('/prediction', methods=['POST'])
def prediction():
    '''
    flask webframe to get medical information for prediction
    '''
    global user_id
    form = request.form
    # get user id
    user_id = request.form['user_id']
    # select or type in a user id
    if user_id:
        # check if this user id in the database
        _, user_id_array = database_query(test_dict, user_id)
        # give a message if this user is in test cases
        if len(user_id_array) != 0:
            message = 'Your user id is %s' %user_id
        # give an error message if this user is not in the test cases
        else:
            message = 'Error: the user id is not found, \n' + \
                      'please enter the correct id or enter as a new user'
            return render_template('index.html', message = message)
    # add a new user/customer
    else:
        user_id = str(database_length(test_dict) + 1)
        message = 'Your assigned user id is %s' %user_id
    # query the medical information for this user
    history_info_query, _= database_query(test_dict, user_id)
    # if there is no information there, suggesting this is a new user and assign
    # an empty string to the textarea
    if len(history_info_query) == 0:
        info = ['']
    # retrieve medical info from test cases and show it in the textarea
    else:
        info = history_info_query
    # pass message and medical information to frontend
    return render_template('prediction.html', form = form, message = message, 
                           info = info)


@app.route('/predictionResults', methods=['POST'])
def predictionResults():
    '''
    flask webframe to predict and display prediction results
    '''
    risks = []
    form = request.form
    # get medical information from textarea in frontend
    history_info = request.form['history_info']
    # retrieve medical information from test cases
    history_info_query, user_id_array = database_query(test_dict, user_id)
    
    error = 'Submission Failed: field must be at least 10 characters long.\n' + \
             'Please enter more information.'
             
    if request.method == 'POST':
        # set condition that at least 10 characters should be typed in
        if len(history_info) < 10:
            return render_template('prediction.html', form = form, 
                                   info = [''], error = error)
        # only add new users' information in order to protect the test cases, 
        # this constrait can be removed for real web page 
        if int(user_id) > 100:
            database_update(test_dict, history_info, user_id)
        # predict probability of risk of stroke based on the input medical information
        t_feature, results = predict(history_info, clf, t_vector, labels, model)
        # get feature information from input medical information
        risk_info = t_vector.inverse_transform(t_feature)[0]
        # check if the features are listed as risk factors
        for rf in risk_factors:
            if rf[0] in risk_info:
                risks.append((rf[1], rf[2]))
        # transfer predict result, medical information and risk factor to frontend
        return render_template('predictionResults.html', form = form, 
                               results = results, history_info = history_info, 
                               factors = risks)
    return render_template('prediction.html', form = form)
       
@app.route('/about_me', methods=['POST'])
def about_me():
    '''
    load About page
    '''
    return render_template('about_me.html')
    
@app.route('/about_sws', methods=['POST'])
def about_sws():
    '''
    load SWS page
    '''
    return render_template('about_sws.html')

'''
The following code is used to avoid cache busting for static template
'''    
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
    # run the app at host site
    app.run(host='0.0.0.0', port=5000, debug = True)