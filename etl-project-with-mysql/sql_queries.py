# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS songplays"
time_table_drop = "DROP TABLE IF EXISTS songplays"

# CREATE TABLES

songplay_table_create = (""" CREATE TABLE IF NOT EXISTS songplays(auto_increment INT, songplay_id bigint, \
                             start_time timestamp NOT NULL, \
                             user_id int REFERENCES users (user_id), \
                                 level varchar(45), song_id varchar(45), \
                                artist_id varchar(45), session_id int, \
                                    location varchar(50) NOT NULL, \
                                        user_agent varchar(500), PRIMARY KEY (auto_increment, songplay_id, session_id))

""")

user_table_create = (""" CREATE TABLE IF NOT EXISTS users (auto_increment INT, user_id INT, \
                     first_name VARCHAR(45) NOT NULL, last_name VARCHAR(45) NOT NULL, gender VARCHAR(45), \
                         level VARCHAR(45), PRIMARY KEY(auto_increment, user_id, last_name))
""")

song_table_create = (""" CREATE TABLE IF NOT EXISTS songs (auto_increment INT, song_id varchar(50), title varchar(100), \
                         artist_id varchar(100), year int NOT NULL, duration decimal(20,10) NOT NULL, \
                             PRIMARY KEY(auto_increment, song_id))
""")

artist_table_create = (""" CREATE TABLE IF NOT EXISTS artists (auto_increment INT, artist_id varchar(45), name varchar(500), \
                           location varchar(100), latitude decimal(10,2), longitude decimal(20,10), \
                               PRIMARY KEY(auto_increment, artist_id, name, location))
""")

time_table_create = (""" CREATE TABLE IF NOT EXISTS time (start_time timestamp NOT NULL, \
                     hour int NOT NULL, day int NOT NULL, week int NOT NULL, month int NOT NULL, \
                         year int NOT NULL, weekday varchar(100) NOT NULL)
""")

# INSERT RECORDS

songplay_table_insert = (""" INSERT INTO songplays(auto_increment, songplay_id, \
                             start_time, user_id, level, song_id, \
                             artist_id, session_id, location, \
                            user_agent) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = (""" INSERT INTO users (auto_increment, user_id, first_name, \
                         last_name, gender, level) VALUES(%s, %s, %s, %s, %s, %s)
""")

song_table_insert = (""" INSERT INTO songs (auto_increment, song_id, title, \
                         artist_id, year, duration) VALUES(%s, %s, %s, %s, %s, %s)
""")

artist_table_insert = (""" INSERT INTO artists (auto_increment, artist_id, name, \
                           location, latitude, longitude) VALUES(%s, %s, %s, %s, %s, %s)
""")


time_table_insert = (""" INSERT INTO time (start_time, hour, \
                         day, week, month, year, weekday) VALUES(%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = (""" SELECT artists.artist_id, songs.song_id FROM (songs JOIN artists ON \
                       artists.artist_id = songs.artist_id) \
                       WHERE songs.title='{}' AND artists.name = '{}' AND songs.duration = {}
""")

# QUERY LISTS

create_table_queries = [user_table_create, artist_table_create, song_table_create,
                        time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop,
                      artist_table_drop, time_table_drop]
