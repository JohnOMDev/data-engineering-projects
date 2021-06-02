#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 23:36:27 2021

@author: john
"""
import psycopg2 as pg
import configparser
from sql_queries import create_table_queries, drop_table_queries

"""
    PLEASE INSERT YOUR REDSHIFT USERNAME, PASSWORD, ENDPOINT AND DATABASE BELOW
"""

def drop_tables(cur, conn):
    """

    Parameters
    ----------
    cur : Connnection
    conn : Connnection

-    Drops each table using the queries in `drop_table_queries` list.
    Returns
    -------
    None.

    """
    for query in drop_table_queries:
        # query = drop_table_queries[0]
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """

    Parameters
    ----------
    cur : Connnection
    conn : Connnection

-   Creates each table using the queries in `create_table_queries` list.
    Returns
    -------
    None.

    """
    for query in create_table_queries:
        # query = create_table_queries[0]
        cur.execute(query)
        conn.commit()


def main():
    """

    Returns
    -------
    - Establishes connection with the exporo database and gets
    cursor to it.
    - Drops all the tables.

    - Creates all tables needed.

    - Finally, closes the connection.
    """

    config = configparser.ConfigParser()
    config.read('dwh.cfg')
# =============================================================================
#     conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))
#     cur = conn.cursor()
# =============================================================================

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

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()