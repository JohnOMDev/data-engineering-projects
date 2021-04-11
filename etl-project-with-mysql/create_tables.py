import mysql.connector as mysql
from mysql.connector import errorcode
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """

    Returns
    -------
    cur : TYPE
        DESCRIPTION.
    conn : TYPE
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """

    # connect to default database
    try:
        db = mysql.connect(user='root', password='***',
                           host="127.0.0.1")
        cursor = db.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("There is error with the username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    

    # create sparkify database with UTF8 encoding
    cursor.execute("DROP DATABASE IF EXISTS ***")

    cursor.execute("CREATE DATABASE IF NOT EXISTS *** \
                   DEFAULT CHARACTER SET utf8 \
                       DEFAULT COLLATE utf8_general_ci")

    # close connection to default database
    db.close()


    # connect to sparkify database
    try:
        db = mysql.connect(user='root', password='***',
                           host="127.0.0.1", database="***")
        cursor = db.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("There is error with the username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    return cursor, db


def drop_tables(cursor, db):
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
        cursor.execute(query)
        db.commit()


def create_tables(cursor, db):
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
        cursor.execute(query)
        db.commit()


def main():
    """

    Returns
    -------
    - Drops (if exists) and Creates the database.

    - Establishes connection with the database and gets
    cursor to it.

    - Drops all the tables.

    - Creates all tables needed.

    - Finally, closes the connection.
    """
    cursor, db = create_database()

    drop_tables(cursor, db)
    create_tables(cursor, db)

    db.close()


if __name__ == "__main__":
    main()
