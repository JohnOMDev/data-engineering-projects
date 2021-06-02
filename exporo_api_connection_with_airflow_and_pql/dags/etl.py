#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 23:38:45 2021

@author: john
"""
import configparser
import psycopg2 as pg
from sql_queries import insert_table_queries

"""
    PLEASE INSERT YOUR REDSHIFT USERNAME, PASSWORD, ENDPOINT AND DATABASE BELOW
"""

def insert_tables(cur, conn):
    """

    Parameters
    ----------
    cur : Connnection

    conn : Connnection
- Loop through the `insert_table_queries` and select data from stagging table and insert the table.

    Returns
    -------
    None.

    """
    for query in insert_table_queries:
        # query = insert_table_queries[0]
        cur.execute(query)
        conn.commit()


def main():
    """

    - Process and call the function
    -------
    None.

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
    insert_tables(cur, conn)

    conn.close()


