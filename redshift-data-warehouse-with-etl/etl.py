import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """

    Parameters
    ----------
    cur : Connnection

    conn : Connnection
- Loop through the `copy_table_queries` and copy the csv from s3 into the stagging tables

    Returns
    -------
    None.

    """
    for query in copy_table_queries:
        # query = copy_table_queries[0]
        cur.execute(query)
        conn.commit()


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

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

