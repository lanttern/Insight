#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 12:47:58 2017

@author: zhihuixie
"""
# import libraries
import wikipedia as wiki
from bs4 import BeautifulSoup
import urllib2
import re
from sklearn.externals import joblib

class MedDictGenerator():
    """
    this class creates a dictionary with key as a medical abbreviation and value as a 
    full term of the abbreviation using resource from wiki page
    """
    def __init__(self, titles):
        """
        @titles - a list of wiki searching keywords
        """
        self.titles = titles

    def med_dict_generator(self):
        """
        create a dictionary with key as a medical abbreviation and value as a 
        full term of the abbreviation using resource from wiki page
        return a dictionary with key as abbreviation of medical terms and value as 
        full term of the abbreviation
        """
        med_dict = {}
        for title in self.titles:
            # get wiki link
            med_abbr = wiki.page(title)
            link = med_abbr.url
            # request content from wiki page
            req = urllib2.Request(link)
            page = urllib2.urlopen(req)
            soup = BeautifulSoup(page, "lxml")
            # processing the content
            table = soup.find('table', { 'class' : 'wikitable sortable' })
            for row in table.findAll('tr'):
                cells = row.findAll('td')
                try:
                    # get the medical abbreviation
                    key = cells[0].find(text = True).encode('utf-8')
                    key = re.sub(' +', ' ', key)
                    # get the corresponding full medical terms and clean the values
                    values = cells[1].findAll(text = True)
                    value = ' '.join([v.lower() for v in values])
                    value = value.split('\n')[0].strip().encode('utf-8')
                    value = re.sub('\(.*?\)', ' ', value)
                    value = re.sub('[^0-9a-zA-Z]', ' ', value)
                    value = re.sub('[ ]+', ' ', value)
                    if (len(key) > 1 and key != 'on' )and key not in med_dict:
                        med_dict[key] = value
                except IndexError:
                    continue
        return med_dict

if __name__ == '__main__':
    # generate wiki search terms
    stem_title = 'List_of_medical_abbreviations:'  
    tails = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    titles = [stem_title + '_' + tails[i] for i in range(len(tails))]
    titles.append(stem_title + '_0-9')
    # generate medical abbreviation-full term dictionary
    generator = MedDictGenerator(titles)
    med_dict = generator.med_dict_generator()
     
    # test the med_dict
    test_cases = ['3TC', 'HLD', 'HTN', 'PCa']
    test_res = []
    res = ['lamivudine', 'Hyperlipidemia', 'hypertension', 'prostate cancer']
    for key in test_cases:
        val = med_dict[key]
        test_res.append(val)
    assert(test_res == res)
    # save data
    joblib.dump(med_dict, '../DataSet/med_dict.plk')
