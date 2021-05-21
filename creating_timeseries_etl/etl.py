#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 17:24:52 2021
#################################################################################
   Processing the files to clean and export the csv file into postgresql tables.
#################################################################################
@author: john
"""
import os
import csv
import json
import logging
import glob
import psycopg2
from datetime import datetime
from sql_queries import crm_table_insert, sales_table_insert

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("etl-process")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))


def process_sales_file(cur, filepath):
    """

    Parameters
    ----------
    cur : TYPE
        DESCRIPTION.
    filepath : TYPE

    Returns
    -------
    - Load the data file
    - Process and insert sales data
    - Process and insert sales data
    """
    # open sales file
    try:
        with open(filepath) as file:
            data = json.load(file)
            sales = json.loads(data[0])
            for row in sales:
                # row = sales[0]
                sale_data = list(row.values())
                # insert sales record
                cur.execute(sales_table_insert, sale_data)
    except Exception as e:
        LOG.exception(f"Problem extracting th neccessary fields {e}")


def process_crm_file(cur, filepath):
    """

    Parameters
    ----------
    cur : TYPE
        DESCRIPTION.
    filepath : TYPE

    Returns
    -------
    - Load the data file
    - Process and insert sales data

    """
    # reading crm file
    with open(filepath, 'r', encoding='utf8', newline='') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        next(csvreader)

        # extracting each data row one by one and append it
        for row in csvreader:
            # line = csvreader[0]
            cur.execute(crm_table_insert, row)


def extract_data(cur, conn, filepath, func_sales, func_crm):
    """

    Parameters
    ----------
    cur : TYPE
    conn : TYPE
    filepath : TYPE
    func_crm : TYPE
    func_sales : TYPE

    Returns
    -------
    - call the process_sales_file func_sales
    - call the process_crm_file func_crm

    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.*'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        # print(i, datafile)
        if datafile.endswith(".csv"):
            func_crm(cur, datafile)
        else:
            func_sales(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    start_time = datetime.now()
    conn = psycopg2.connect("host=127.0.0.1 dbname=market_shares user=* password=*")
    cur = conn.cursor()

    LOG.info(os.getcwd())
    filepath = os.getcwd() + '/data-engineer-task-data/data/'

    extract_data(cur, conn, filepath, func_sales=process_sales_file, func_crm=process_crm_file)

    conn.close()
    end_time = datetime.now() - start_time
    LOG.info("It took %s to process and load the data into database" % end_time)


if __name__ == "__main__":
    main()

