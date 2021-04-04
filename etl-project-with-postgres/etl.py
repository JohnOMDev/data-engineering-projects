import os
import glob
import psycopg2
from datetime import datetime
import pandas as pd

# from sql_queries import *  # Bad code using wildcard
from sql_queries import songplay_table_insert, user_table_insert, song_table_insert, \
                            artist_table_insert, time_table_insert, song_select


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_cols = ["song_id", "title", "artist_id", "year", "duration"]
    song_data = df[song_cols]
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_col = ["artist_id", "artist_name", "artist_location",
                  "artist_latitude", "artist_longitude"]
    artist_data = df[artist_col].rename(columns={"artist_name": "name",
                                                 "artist_location": "location",
                                                 "artist_latitude": "latitude",
                                                 "artist_longitude": "longitude"
                                                 })
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
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
        print(list(row))
        cur.execute(time_table_insert, list(row))

    # load user table
    user_cols = ["userId", "firstName",
                 "lastName", "gender", "level"]
    user_df = df[user_cols].rename(columns=({
        "userId": "user_id",
        "firstName": "first_name",
        "lastName": "last_name"
        }))
    user_df["user_id"] = user_df["user_id"].astype(int)

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
        song_cols = ["songplay_id", "start_time", "user_id", "level", "song_id",
                     "artist_id", "session_id", "location", "user_agent"]
        # insert songplay record
        songplay_data = 
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
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
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
