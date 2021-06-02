#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 06:40:46 2021

@author: john
"""
# import sys
# import json
# import datetime

import pandas as pd
import logging
import os
import numpy as np
import psycopg2 as pg
import configparser
from sql_queries import investment_table_insert

# exporo client
from exporo_api import ExporoAPI
logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("api_connector.py")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))

"""
    PLEASE INSERT YOUR REDSHIFT USERNAME, PASSWORD, ENDPOINT AND DATABASE BELOW
"""

config = configparser.ConfigParser()
config.read('dwh.cfg')
    # attempt the connection to postgres
try:
    conn = pg.connect(
        database=config.get("DB", "db_name"),
        user=config.get("DB", "db_user"),
        password=config.get("DB", "db_password"),
        host=config.get("DB", "host")
    )
    cur = conn.cursor()
except Exception as error:
    print(error)

def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No data downloaded. Finishing execution")
        return False 

    # Primary Key Check
    if pd.Series(df['Financing Entity ID']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")
    return True

def get_exporo_data_to_df():
    """

    Parameters
    ----------

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    cols = ['hash', 'title', 'financingEntityId', 'contractId', 'image', 'investmentRate',
            'investmentType', 'minimumInvestment', 'durationInvestorMin',
            'durationInvestorMax', 'maximumInvestment', 'startDate']
    
    rename_cols = {
        'hash': 'ID', 'title': 'Name', 'financingEntityId':'Financing Entity ID',
        'contractId': 'Contract ID', 'image': 'Image', 'investmentRate': 'Investment Rate',
        'investmentType':'Investment Type', 'minimumInvestment':'Minimum Investment',
        'durationInvestorMin': 'Duration Investor Min',
        'durationInvestorMax': 'Duration Investor Max', 'maximumInvestment': 'Maximum Investment',
        'startDate':'Date'
        }
    # connect to your api class
    try:
        exporo_api_handler = ExporoAPI()

        df = exporo_api_handler.get_api_details()
    
        if len(df.index) > 0:
            df = df[cols].rename(columns=rename_cols)
        else:
            LOG.exception("No data was return for endpoint")

        df = df.replace(np.nan, '', regex=True)
        df["Investment Rate"] = df["Investment Rate"].apply(lambda x:x.replace(",",".").split(' ')[0])
        df["Minimum Investment"] = df["Minimum Investment"].apply(lambda x:x.split(' ')[0])
        df["Maximum Investment"] = df["Maximum Investment"].apply(lambda x:x.split(' ')[0])
        df["Date"] = df["Date"].apply(lambda x:x.replace(","," ").replace("Invalid", "").split(' ')[0])
        # Validate
        if check_if_valid_data(df):
            print("Data valid, proceed to Load stage")
        # Staging into the Database
        for i, row in df.iterrows():
            # print(list(row))
            cur.execute(investment_table_insert, list(row))
            conn.commit()
        conn.close()
    except:
        LOG.exception("There were some error when accessing the endpoint")
        conn.close()
    return df

    
    
