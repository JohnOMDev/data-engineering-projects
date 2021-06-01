#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 23:38:45 2021

@author: john
"""
import configparser
import psycopg2
from sql_queries import insert_table_queries

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

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}")
    cur = conn.cursor()

    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

