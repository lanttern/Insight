#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: zhihuixie
this program is used to sample out discharge summary for note events table
"""
import pandas as pd
# set up path to read file and path to output file
in_file_name = '../DataSet/NOTEEVENTS.csv'
out_file_name = '../DataSet/note_events_discharge.csv'
# set up column names to get data
cols = ['SUBJECT_ID', 'HADM_ID', 'CATEGORY', 'ISERROR', 'TEXT']
# iterate and process 500000 rows from data each time and retrieve discharge summary category
iter_csv = pd.read_csv(in_file_name, iterator=True, chunksize = 500000, usecols = cols)
print 'Compelte loading data and starting to processing!'
df = pd.concat([chunk[chunk['CATEGORY'] == 'Discharge summary'] for chunk in iter_csv])
print 'Complete processing!'
# write data in pandas dataframe to a csv file
df.to_csv(out_file_name, index = False)
print 'Data are written successfully!'
