#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: zhihuixie
"""
import pandas as pd

class Sampling():
    """
    this program is used to sample out discharge summary for note events table
    """
    def __init__(self, in_file_name, out_file_name):
        """
        initiate two parameters:
            @in_file_name: file name of input data
            @out_file_name: file name of output data
        """
        self.in_file_name = in_file_name
        self.out_file_name = out_file_name
        
    def read_file(self, cols, chunksize):
        """
        read a file into pandas dataframe with the chuncksize
        @cols: cols used to extract
        @chunksize: size of chunks to read into the dataframe
        """
        self.iter_csv = pd.read_csv(in_file_name, iterator=True, 
                                    chunksize = chunksize, usecols = cols)
        print 'Compelte loading data and starting to processing!'
        
    def save_file(self, col_value, col_name, cols, chunksize):
        """
        save to file to local
        @col_value: filter to get the target rows
        @col_name: filter to target to the specific column
        @cols: cols used to extract
        @chunksize: size of chunks to read into the dataframe
        """
        self.read_file(cols, chunksize)
        df = pd.concat([chunk[chunk[col_name] == col_value] for chunk in self.iter_csv])
        print 'Complete processing!'
        df.to_csv(self.out_file_name, index = False)
        print 'Data are written successfully!'

if __name__ == "__main__":
    # set up path to read file and path to output file
    in_file_name = '../DataSet/NOTEEVENTS.csv'
    out_file_name = '../DataSet/note_events_discharge.csv'
    # set up column names to get data
    cols = ['SUBJECT_ID', 'HADM_ID', 'CATEGORY', 'ISERROR', 'TEXT']
    chunksize = 500000
    col_name = 'CATEGORY'
    col_value = 'Discharge summary'
    sample = Sampling(in_file_name, out_file_name)
    sample.save_file(col_value, col_name, cols, chunksize)
