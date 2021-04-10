#!/usr/bin/env python
# coding: utf-8

# Import Python packages 
"""
Created on Sat Apr 10 19:21:27 2021

@author: john
"""
import os
import glob
import csv
import logging
logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("etl-process.py")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))

"""
   Processing the files to create the data file csv that will be used \
    for Apache Casssandra tables.
 
   Creating list of filepaths to process original event csv data files
"""

# checking your current working directory
LOG.info(os.getcwd())

# Create a for loop to create a list of files and collect each filepath
filepath = os.getcwd() + '/event_data'
for root, dirs, files in os.walk(filepath):

    file_path_list = glob.glob(os.path.join(root,'*.csv'))



# initiating an empty list of rows that will be generated from each file
full_data_rows_list = [] 
    
# for every filepath in the file path list 
for f in file_path_list:
    try:
# reading csv file 
        with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
            next(csvreader)
            
            # extracting each data row one by one and append it        
            for line in csvreader:
                full_data_rows_list.append(line)
    except:
        LOG.exception("Problem extracting the file")


# =============================================================================
#  creating a smaller event data csv file called event_datafile_full csv \
#    that will be used to insert data into the \
#  Apache Cassandra tables
# =============================================================================


csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)
try:
    with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(['artist','firstName','gender','itemInSession','lastName',
                         'length', 'level','location','sessionId','song','userId'])
        for row in full_data_rows_list:
            if (row[0] == ''):
                continue
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))
except:
    LOG.exception("Problem creating the smaller event csv")
