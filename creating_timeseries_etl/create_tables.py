#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 19:57:38 2021

@author: john
"""

import psycopg2
from sql_queries import create_table_queries, drop_table_queries


"""
    PLEASE INSERT YOUR POSTGRESQL USERNAME, PASSWORD AND DATABASE BELOW
"""


def create_database():
    """

    Returns
    -------
    cur : TYPE
    conn : TYPE
    - Creates and connects to the housing
    - Returns the connection and cursor to housingdb
    """

    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=my_first_db user=* password=*")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create housing database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS market_shares")
    cur.execute("CREATE DATABASE market_shares WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to housing database
    conn = psycopg2.connect("host=127.0.0.1 dbname=market_shares user=* password=*")
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """

    Parameters
    ----------
    cur : TYPE
        DESCRIPTION.
    conn : TYPE
        DESCRIPTION.

    Returns
    -------
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        # query = drop_table_queries[0]
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """

    Parameters
    ----------
    cur : TYPE
    conn : TYPE


    Returns
    -------
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        # query = create_table_queries[0]
        cur.execute(query)
        conn.commit()


def main():
    """

    Returns
    -------
    - Drops (if exists) and Creates the housing database.

    - Establishes connection with the housing database and gets
    cursor to it.

    - Drops all the tables.

    - Creates all tables needed.

    - Finally, closes the connection.
    """
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
