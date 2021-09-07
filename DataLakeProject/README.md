## Sparkify Data Lake Project
### Sparkify is a music streaming platform and due to their growing user base they want to move their data warehouse to a data lake

**Their current data is currently in S3 in the form of song metadata and user logs**
## Star Schema (Fact and Dimensional Tables)
### FACT TABLE
**songplays** - table to hold all the data for each songplay in the sparkify app and connect all the attributes to their respective dimension table where additional information is held

	songplay_id
    start_time
    user_id
    level
    song_id
    artist_id
    session_id
    location
    user_agent

### DIMENSION TABLES

**users** - users in the app

	user_id
    first_name
    last_name
    gender
    level

**songs** - songs in music database

	song_id
    title
    artist_id
    year
    duration

**artists** - artists in music database

	artist_id
    name
    location
    latitude
    longitude

**time** - timestamps of records in songplays broken down into specific units

	start_time
    hour
    day
    week
    month
    year
    weekday
## DATA:

**log_data:** a collection of Json files that log the users interacting with the application.

	ex: {"artist":"The Grass Roots","auth":"Logged In","firstName":"Sara","gender":"F","itemInSession":72,"lastName":"Johnson","length":166.71302,"level":"paid","location":"Winston-Salem, NC","method":"PUT","page":"NextSong","registration":1540809153796.0,"sessionId":411,"song":"Let's Live For Today","status":200,"ts":1542153802796,"userAgent":"\"Mozilla\/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit\/537.51.2 (KHTML, like Gecko) Version\/7.0 Mobile\/11D257 Safari\/9537.53\"","userId":"95"}

**song_data**: a collection of song data that has important attributes for the songs. In JSON format

	ex:{"num_songs": 1, "artist_id": "ARGCY1Y1187B9A4FA5", "artist_latitude": 36.16778, "artist_longitude": -86.77836, "artist_location": "Nashville, TN.", "artist_name": "Gloriana", "song_id": "SOQOTLQ12AB01868D0", "title": "Clementina Santaf\u00e8", "duration": 153.33832, "year": 0}

## ETL:
 
**The ETL works as so...**
In the script etl.py we **extract** the data from S3 and process it using a spark cluster in AWS EMR. After loading the data the necessary **transformations** are made to organize, reformat, and select/join the needed columns and tables together. Once transformed the data is **loaded** back to S3 in parquet files.

## Files:
**etl.py** 
This file is where the ETL logic occurs, the main function calls helper functions that extract, transform then load the data back to S3 in its knew structured format

## How to run it 
I run this file in a notebook on an EMR cluster. In order to do so log into your AWS account and create a EMR cluster with Spark. Create a notebook that is attached to this cluster and upload the etl.py to it. Simply running that notebook will perform the logic.