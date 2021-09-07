import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Load the data from S3 into a dataframe to extract the needed columns
    Select the needed columns for the songs_table and artists_table
    write songs_table to parquet files in s3
    write artists_table to parquet files in s3
    
    Parameters
    ----------
    spark: session
           spark session that has been created
    input_data: path
            path to the udacity song_data s3 bucket.
    output_data: path
            path to where the files will be written.
    """
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    # drop duplicates
    songs_table = df.select(['song_id','title','artist_id','year','duration']).dropDuplicates()
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.parquet(os.path.join(output_data, 'songs'), partitionBy=['year', 'artist_id'])

    # extract columns to create artists table 
    # drop duplicates
    artists_table =     df.select(['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']) \
                      .withColumnRenamed('artist_name', 'name') \
                      .withColumnRenamed('artist_location', 'location') \
                      .withColumnRenamed('artist_latitude', 'latitude') \
                      .withColumnRenamed('artist_longitude', 'longitude') \
                      .dropDuplicates()
    
    # write artists table to parquet files
    artists_table.write.parquet(os.path.join(output_data, 'artists'))


def process_log_data(spark, input_data, output_data):
    """
    Load the data from S3 into a dataframe to extract the needed columns
    Select the needed columns for the users_table, time_table, songplays_table
    
    write users_table to parquet files in s3
    write time_table to parquet files in s3
    write songplays_table to parquet files in s3
    
    Parameters
    ----------
    spark: session
           spark session that has been created
    input_data: path
            path to the udacity log_data s3 bucket.
    output_data: path
            path to where the files will be written.
    """
    # get filepath to log data file
    log_data = input_data + 'log_data/*/*/*/*.json'

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table    
    users_table = df.select(['ts','userId','level','song','artist','sessionId','location','userAgent'])
    
    # write users table to parquet files
    users_table.write.parquet(os.path.join(output_data, 'users'))

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: str(int(int(x)/1000)))
    df = df.withColumn('timestamp',get_timestamp(df.ts))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: str(datetime.fromtimestamp(int(x) / 1000.0)))
    df = df.withColumn("datetime", get_datetime(df.ts))
    
    # extract columns to create time table
    time_table = df.select(
        col('datetime').alias('start_time'),
        hour('datetime').alias('hour'),
        dayofmonth('datetime').alias('day'),
        weekofyear('datetime').alias('week'),
        month('datetime').alias('month'),
        year('datetime').alias('year'),
        dayofweek('datetime').alias('weekday')
    )
    
    # write time table to parquet files partitioned by year and month
    time_table.write.parquet(os.path.join(output_data, 'time'), partitionBy=['year', 'month'])

    # read in song data to use for songplays table
    song_df = spark.read.json(input_data + 'song_data/*/*/*/*.json')

    # create views of song_df and event data to use SQL to join into fact table
    song_df.createOrReplaceTempView('songs')
    df.createOrReplaceTempView('events')
    
    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = spark.sql(
    '''SELECT
            e.songplay_id,
            e.start_time,
            e.user_id,
            e.level,
            s.song_id,
            s.artist_id,
            e.sessionId as session_id,
            e.location,
            e.userAgent as user_agent,
            year(e.start_time) as year,
            month(e.start_time) as month
        FROM events e
        LEFT JOIN songs s ON
            e.song = s.title AND
            e.artist = s.artist_name 
    ''')

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.parquet(os.path.join(output_data, 'songplays'), partitionBy=['year', 'month'])


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3://dvz-sparkify-data/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
