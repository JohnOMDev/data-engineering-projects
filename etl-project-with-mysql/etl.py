import os
import glob
from datetime import datetime
import pandas as pd
import mysql.connector as mysql
from mysql.connector import errorcode
import logging
logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("etl.py")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))
from sql_queries import songplay_table_insert, user_table_insert, song_table_insert, \
                            artist_table_insert, time_table_insert, song_select

"""
    PLEASE INSERT YOUR MYSQL USERNAME, PASSWORD AND DATABASE BELOW
"""
def process_song_file(cursor, filepath):
    """

    Parameters
    ----------
    cursor : TYPE
        DESCRIPTION.
    filepath : TYPE

    Returns
    -------
    - Load the data file
    - Process and insert song data
    - Process and insert artist data

    """
    # open song file
    df = pd.read_json(filepath, lines=True)
    df = df.where((pd.notnull(df)), None)
    # insert song record
    song_data_df = df[["song_id", "title", "artist_id", "year", "duration"]]
    for i in song_data_df.index:
        row = song_data_df.iloc[i]
        Selected_list = [i, int(row['song_id']), row['title'], \
                             int(row['artist_id']), int(row['year']), float(row['duration'])]
        #  LOG.info(Selected_list)
        cursor.execute(song_table_insert, Selected_list)

    artist_data_df = df[["artist_id", "artist_name", "artist_location",
                         "artist_latitude", "artist_longitude"]]
    for i in artist_data_df.index:
        row = artist_data_df.iloc[i]
        Selected_list = [i, int(row['artist_id']), row['artist_name'], \
                             row['artist_location'], float(row['artist_latitude']),
                             float(row['artist_longitude'])]
        #  LOG.info(Selected_list)
        cursor.execute(artist_table_insert, Selected_list)


def process_log_file(cursor, filepath):
    """

    Parameters
    ----------
    cursor : TYPE
        DESCRIPTION.
    filepath : TYPE

    Returns
    -------
    - Load the data file
    - Process and insert user data
    - Process and insert time data
    - Extract artist_id and song_id from artist and song table
    - Process and insert the fact table "songsplay"

    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"] == "NextSong"]
    # convert timestamp column to datetime
    t = df['ts'].apply(lambda x: datetime.utcfromtimestamp(x//1000.0))
    # insert time data records
    df['start_time'] = t
    df['hour'] = t.apply(lambda x: x.hour)
    df['day'] = t.apply(lambda x: x.day)
    df['week'] = t.apply(lambda x: x.week)
    df['month'] = t.apply(lambda x: x.month)
    df['year'] = t.apply(lambda x: x.year)
    df['weekday'] = t.apply(lambda x: x.day_name())
    column_labels = ["start_time", "hour",
                     "day", "week", "month", "year", "weekday"]
    time_df = df[column_labels]

    for i, row in time_df.iterrows():
        LOG.info(list(row))
        cursor.execute(time_table_insert, list(row))

    # load user table
    user_cols = ["userId", "firstName",
                 "lastName", "gender", "level"]
    user_df = df[user_cols].rename(columns=({
        "userId": "user_id",
        "firstName": "first_name",
        "lastName": "last_name"
        }))
    user_df["user_id"] = user_df["user_id"].astype(int)
    user_df.reset_index(drop=True, inplace=True)
    # insert user records

    for i in user_df.index:
        row = user_df.iloc[i]
        Selected_list = [i, int(row['user_id']), row['first_name'], \
                             row['last_name'], row['gender'], row['level']]
        #  LOG.info(Selected_list)
        cursor.execute(user_table_insert, Selected_list)

    for index, row in df.iterrows():
        # row = df.iloc[1]
        # get songid and artistid from song and artist tables

        insert_statement = song_select.format(*(row.song.replace("'", ""),
                                                row.artist.replace("'", ""), row.length))
        cursor.execute(insert_statement)
        results = cursor.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
        # insert songplay record
        songplay_data = (index, row.ts, row.start_time, int(row.userId), row.level, songid, artistid,
                         row.sessionId, row.location, row.userAgent)
        cursor.execute(songplay_table_insert, songplay_data)


def process_data(cursor, db, filepath, func):
    """

    Parameters
    ----------
    cursor : TYPE
    db : TYPE
    filepath : TYPE
        DESCRIPTION.
    func : TYPE

    Returns
    -------
    - call the process_song_file func
    - call the process_log_file func

    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cursor, datafile)
        db.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    try:
        db = mysql.connect(user='root', password='***',
                       host="127.0.0.1", database="***")
        cursor = db.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
             LOG.info("There is error with the username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
             LOG.info("Database does not exist")
        else:
             LOG.info(err)
    process_data(cursor, db, filepath='data/song_data', func=process_song_file)
    process_data(cursor, db, filepath='data/log_data', func=process_log_file)

    db.close()


if __name__ == "__main__":
    main()
