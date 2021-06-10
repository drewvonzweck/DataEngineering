import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    
    """
    Description:
        Parses all the json data from the files that are found in the song_file files.
        This data is transformed using the pandas library and then loaded into the tables songs, and artists
    
    Arguments: 
        cur: the cursor object
        filepath: log data or song data file path.
        
    Returns:
        none
    """
    
    # open song file
    df = pd.read_json(filepath,lines = True)

    # insert song record
    song_data = list(df[["song_id","title","artist_id","year","duration"]].values[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df[["artist_id","artist_name","artist_location","artist_latitude","artist_longitude"]].values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    
    """
    Description:
        Parses all the json data from the files that are found in the log_file files.
        This data is transformed using the pandas library and then loaded into the tables time, user, and song_plays
    
    Arguments: 
        cur: the cursor object
        filepath: log data or song data file path.
        
    Returns:
        none
    """
    
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    t = df.copy()
    
    # insert time data records
    time_data = (t.ts, t.ts.dt.hour , t.ts.dt.day , t.ts.dt.dayofweek , t.ts.dt.month , t.ts.dt.year , t.ts.dt.weekday)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday') 
    time_df = pd.DataFrame(dict(zip(column_labels,time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    # replace the empty userId with userID 00000
    df['userId'] = df['userId'].replace([''],'00000')
    user_df = df[["userId","firstName","lastName","gender","level"]] 

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

        # insert songplay record
        songplay_data = (row.ts, row.userId,row.level, songid, artistid, row.sessionId, row.location, row.userAgent) 
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
   
    """
    Description:
        This function lists all the files in the passed directory and makes the proper calls to each
        It uses the func passed to it to do the proper transformation and loading into the database
    
    Arguments: 
        cur: the cursor object
        conn: the connection to the database
        filepath: log data or song data file path.
        func: the function that does the actual transforming and loading
        
    Returns:
        none
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
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
    """
    Description:
        Makes the connection to the database.
        Creates the conn
        Creates the cursor used to query the database
        Calls the process_data function twice
        Once for each of the directories that contain all the data
        Passing the proper function and the curr and conn
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()