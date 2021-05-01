import configparser

######################################################################## CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

LOG_DATA = config.get("S3","log_data")
SONG_DATA = config.get("S3","song_data")
LOG_JSON_PATH = config.get("S3","log_jsonpath")
DWH_ROLE =config.get("IAM_ROLE", "arn")
################################################################### DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

################################################################# CREATE TABLES

staging_events_table_create= ("""
   CREATE TABLE IF NOT EXISTS staging_events
   (
    staging_event_key BIGINT IDENTITY(0,1) distkey sortkey,
    artist VARCHAR(500),
    auth VARCHAR(45),
    firstName VARCHAR(45),
    gender CHAR(1),
    itemInSession INTEGER,
    lastName VARCHAR(45),
    length DECIMAL(10,5),
    level VARCHAR(45),
    location VARCHAR(500),
    method VARCHAR(45),
    page VARCHAR(45),
    registration BIGINT,
    sessionId INTEGER,
    song VARCHAR(500),
    status INTEGER,
    ts TIMESTAMP,
    userAgent VARCHAR(500),
    userId INTEGER)
""")

staging_songs_table_create = (""" 
   CREATE TABLE IF NOT EXISTS staging_songs
   (
     staging_song_key BIGINT IDENTITY(0,1) sortkey,
     num_songs INTEGER,
     artist_id VARCHAR(100),
     artist_latitude DECIMAL(10,5),
     artist_longitude DECIMAL(10,5),
     artist_location VARCHAR(500),
     artist_name VARCHAR(500),
     song_id VARCHAR(100) distkey,
     title VARCHAR(500),
     duration DECIMAL(10,5),
     year INTEGER
     )
""")

songplay_table_create = ("""
  CREATE TABLE IF NOT EXISTS songplays
  (
    songplay_id INTEGER IDENTITY(0,1),
    start_time TIMESTAMP NOT NULL sortkey distkey,
    user_id INTEGER NOT NULL,
    level VARCHAR(45),
    song_id VARCHAR(100),
    artist_id  VARCHAR(100),
    session_id BIGINT,
    location VARCHAR(500) NOT NULL,
    user_agent VARCHAR(500)
    )
""")

user_table_create = ("""
  CREATE TABLE IF NOT EXISTS users
  (
    user_id INTEGER distkey sortkey,
    first_name VARCHAR(45),
    last_name VARCHAR(45),
    gender CHAR(1),
    level  VARCHAR(45)
    )
""")

song_table_create = ("""
  CREATE TABLE IF NOT EXISTS songs
  (
    song_id VARCHAR(45) distkey sortkey,
    title VARCHAR(500),
    artist_id VARCHAR(100),
    year INTEGER NOT NULL,
    duration DECIMAL(10,5) NOT NULL
    )
""")

artist_table_create = ("""
  CREATE TABLE IF NOT EXISTS artists
  (
    artist_id  VARCHAR(100) distkey sortkey,
    name  VARCHAR(500),
    location  VARCHAR(500),
    latitude DECIMAL(10,5),
    longitude DECIMAL(10,5)
    )
""")

time_table_create = ("""
  CREATE TABLE IF NOT EXISTS time
  (
    date_key INTEGER IDENTITY(0,1),
    start_time TIMESTAMP NOT NULL distkey sortkey,
    hour SMALLINT NOT NULL,
    day SMALLINT NOT NULL,
    week SMALLINT NOT NULL,
    month SMALLINT NOT NULL,
    year SMALLINT NOT NULL,
    is_weekend BOOLEAN NOT NULL
    )
""")

################################################################ STAGING TABLES

staging_events_copy = ("""
   COPY staging_events from '{}'
   credentials 'aws_iam_role={}'
   COMPUPDATE OFF region 'us-west-2'
   TIMEFORMAT as 'epochmillisecs'                         
   TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
    FORMAT AS JSON '{}';
""").format(LOG_DATA, DWH_ROLE, LOG_JSON_PATH)

staging_songs_copy = ("""
    COPY staging_songs from '{}'
    credentials 'aws_iam_role={}'
    COMPUPDATE OFF region 'us-west-2'
    FORMAT AS JSON 'auto' 
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;                                    
""").format(SONG_DATA, DWH_ROLE)

# FINAL TABLES

songplay_table_insert = ("""
   INSERT INTO songplays(start_time, user_id, level,
                         song_id, artist_id, session_id, location, user_agent)
   SELECT se.ts             AS start_time,
          se.userId         AS user_id,
          se.level          AS level,
          ss.song_id        AS song_id,
          ss.artist_id      AS artist_id,
          se.sessionId      AS session_id,
          se.location       AS location, 
          se.userAgent      AS user_agent
   FROM staging_events as se
   JOIN staging_songs as ss ON se.artist = ss.artist_name
   WHERE se.page = 'NextSong'
""")

user_table_insert = ("""
  INSERT INTO users (user_id, first_name, last_name, gender, level)
  SELECT userId            AS user_id,
         firstName         AS first_name,
         lastName          AS last_name,
         gender            AS gender,
         level             AS level
 FROM staging_events

""")

song_table_insert = ("""
  INSERT INTO songs (song_id, title, artist_id, year, duration)
  SELECT song_id       AS song_id,
  title                AS title,
  artist_id            AS artist_id,
  year                 AS year,
  duration             AS duration
  FROM staging_songs
""")

artist_table_insert = ("""
  INSERT INTO artists (artist_id, name, location, latitude, longitude)
  SELECT artist_id          AS artist_id,
         artist_name        AS name,
         artist_location    AS location,
         artist_latitude    AS latitude,
         artist_longitude   AS longitude
  FROM staging_songs
""")

time_table_insert = ("""
  INSERT INTO time (start_time, hour, day, week, month, year, is_weekend)
  SELECT
         TO_TIMESTAMP(ts,'yyy-MM-DD') AS start_time,
         EXTRACT(hour FROM start_time)                AS hour,
         EXTRACT(DAY FROM start_time)                 AS day,
         EXTRACT(WEEK FROM start_time)                AS week,
         EXTRACT(MONTH FROM start_time)               AS month,
         EXTRACT(YEAR FROM start_time)                AS year,
         CASE WHEN EXTRACT(DOW FROM start_time) IN (6, 7) THEN true ELSE false END AS is_weekend
         FROM staging_events
WHERE start_time IS NOT NULL;
""")

################################################################### QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
