import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES(if they exist)

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES (Staging tables & Star Schema for Analytics)

#Staging Table for Events
staging_events_table_create= ("""
CREATE TABLE staging_events(
    event_id INT IDENTITY(0,1),
    artist_name VARCHAR,
    auth VARCHAR,
    user_first_name VARCHAR,
    user_gender VARCHAR,
    item_in_session INTEGER,
    user_last_name VARCHAR,
    song_length DOUBLE PRECISION, 
    user_level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration VARCHAR,
    session_id BIGINT,
    song_title VARCHAR,
    status INTEGER, 
    ts VARCHAR,
    user_agent TEXT,
    user_id VARCHAR,
    PRIMARY KEY (event_id))
""")

#Staging Table for Songs
staging_songs_table_create = ("""
CREATE TABLE staging_songs(
    song_id VARCHAR,
    num_songs INTEGER,
    artist_id VARCHAR,
    artist_latitude DOUBLE PRECISION,
    artist_longitude DOUBLE PRECISION,
    artist_location VARCHAR,
    artist_name VARCHAR,
    title VARCHAR,
    duration DOUBLE PRECISION,
    year INTEGER,
    PRIMARY KEY (song_id))
""")

#Fact Table
songplay_table_create = ("""
CREATE TABLE songplays(
    songplay_id INT IDENTITY(0,1),
    start_time TIMESTAMP NOT NULL,
    user_id VARCHAR NOT NULL,
    level VARCHAR NOT NULL,
    song_id VARCHAR NOT NULL,
    artist_id VARCHAR NOT NULL,
    session_id BIGINT NOT NULL,
    location VARCHAR NOT NULL,
    user_agent TEXT NOT NULL,
    PRIMARY KEY (songplay_id))
""")

#Dimension Table User
user_table_create = ("""
CREATE TABLE users(
    user_id VARCHAR,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    gender VARCHAR(1) NOT NULL,
    level VARCHAR NOT NULL,
    PRIMARY KEY (user_id))
""")

#Dimension Table Song
song_table_create = ("""
CREATE TABLE songs(
    song_id VARCHAR,
    title VARCHAR NOT NULL,
    artist_id VARCHAR NOT NULL,
    year INTEGER NOT NULL,
    duration DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (song_id))
""")

#Dimension Table Artist
artist_table_create = ("""
CREATE TABLE artists(
    artist_id VARCHAR,
    name VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    PRIMARY KEY (artist_id))
""")

#Dimension Table Time
time_table_create = ("""
CREATE TABLE time(
    start_time TIMESTAMP,
    hour INTEGER,
    day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday INTEGER,
    PRIMARY KEY (start_time))
""")

# FILL STAGING TABLES FROM S3

staging_events_copy = ("""copy staging_events 
                          from {}
                          iam_role {}
                          json {};
                       """).format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3','LOG_JSONPATH'))

staging_songs_copy = ("""copy staging_songs 
                          from {} 
                          iam_role {}
                          json 'auto';
                      """).format(config.get('S3','SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FILL FINAL TABLES FROM STAGING TABLES (Star Schema)

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
SELECT DISTINCT
    TIMESTAMP 'epoch' + e.ts/1000 * interval '1 second' as start_time, 
    e.user_id, 
    e.user_level, 
    s.song_id,
    s.artist_id, 
    e.session_id,
    e.location, 
    e.user_agent
FROM staging_events e, staging_songs s
WHERE e.page = 'NextSong' 
AND e.song_title = s.title 
AND e.artist_name = s.artist_name 
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT  
    user_id, 
    user_first_name, 
    user_last_name, 
    user_gender, 
    user_level
FROM staging_events
WHERE page = 'NextSong'
AND user_id IS NOT NULL
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration) 
SELECT DISTINCT 
    song_id, 
    title,
    artist_id,
    year,
    duration
FROM staging_songs
WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude) 
SELECT DISTINCT 
    artist_id,
    artist_name,
    artist_location,
    artist_latitude,
    artist_longitude
FROM staging_songs
WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekDay)
SELECT start_time, 
    extract(hour from start_time),
    extract(day from start_time),
    extract(week from start_time), 
    extract(month from start_time),
    extract(year from start_time), 
    extract(dayofweek from start_time)
FROM songplays
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
