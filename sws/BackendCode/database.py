#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
@author: zhihuixie
'''
'''
import libraries
'''
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

# define username and database name
db_name = 'medical_record'
user_name = 'zhihuixie'

# create engine
engine = create_engine('postgres://%s@localhost/%s'%(user_name, db_name))
print engine.url
if not database_exists(engine.url):
    create_database(engine.url)
# load pandas dataframe to database
df = pd.read_csv('../DataSet/stroke_his_info_db.csv')
print df.columns
df.to_sql('records', engine, if_exists = 'replace')

def database_insert(conn, record, label):  
    '''
    this function insert record and label to the database
    '''
    cur = conn.cursor()
    cur.execute('''INSERT INTO records (TEXT, PRIMARY_DIAGNOSIS) VALUES (%s, %s);''', (record, label))
    conn.commit()
    cur.close()

def database_query(conn, search_text):  
    '''
    this function queries the database based on the search text
    '''
    sql_query = '''
    SELECT * FROM records
    WHERE label LIKE %(%search_text%)s
    LIMIT 10;
    '''
    sql_results = pd.read_sql_query(sql_query, conn, params = {'search_text':search_text})
    results = zip(sql_results['PRIMARY_DIAGNOSIS'].values, \
                  sql_results['LONG_TITLE'].values, \
                  sql_results['ICD9_CODE'].values, \
                  sql_results['TEXT'].values)
    print results

if __name__ == '__main__':
    # test query and insert new data into the database
    conn = None
    conn = psycopg2.connect(database = db_name, user = user_name)  
    database_query(conn, 'test')
    database_insert(conn, 'this is a test number', 'test')
    database_query(conn, 'test')
    conn.close()