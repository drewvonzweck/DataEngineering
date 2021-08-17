# PROJECT 3: Data Warehouse in AWS

## WHAT IS SPARKIFY?

**We are creating a DW for Sparkify**, which is a music streaming application. They wish to better understand what songs their users are listening to. For this we need to organize their data into a DataWarehouse. This data warehouse will use the Star Schema to be optimized for analytic queries.

## DW TABLES :

### STAGING TABLES
**staging_events** - table to hold the data from the raw files... events that represent users interacting with Sparkify

	event_id
	artist_name
    auth 
    user_first_name 
    user_gender 
    item_in_session 
    user_last_name 
    song_length  
    user_level 
    location 
    method 
    page 
    registration 
    session_id 
    song_title 
    status  
    ts 
    user_agent 
    user_id

**staging_songs** - table to hold the data from the raw files...songs and their respective attributes from the sparkify app 

	song_id
    num_songs
    artist_id
    artist_latitude
    artist_longitude
    artist_location
    artist_name
    title
    duratio
    year
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

> **Note:** These tables are in a Star Schema and provide a clear division of entities and give the ability to split the given data sets into a logical set of relations

## DATA:

**log_data:** a collection of Json files that log the users interacting with the application.

	ex: {"artist":"The Grass Roots","auth":"Logged In","firstName":"Sara","gender":"F","itemInSession":72,"lastName":"Johnson","length":166.71302,"level":"paid","location":"Winston-Salem, NC","method":"PUT","page":"NextSong","registration":1540809153796.0,"sessionId":411,"song":"Let's Live For Today","status":200,"ts":1542153802796,"userAgent":"\"Mozilla\/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit\/537.51.2 (KHTML, like Gecko) Version\/7.0 Mobile\/11D257 Safari\/9537.53\"","userId":"95"}

**song_data**: a collection of song data that has important attributes for the songs. In JSON format

	ex:{"num_songs": 1, "artist_id": "ARGCY1Y1187B9A4FA5", "artist_latitude": 36.16778, "artist_longitude": -86.77836, "artist_location": "Nashville, TN.", "artist_name": "Gloriana", "song_id": "SOQOTLQ12AB01868D0", "title": "Clementina Santaf\u00e8", "duration": 153.33832, "year": 0}

## ETL:
 
**The ETL works as so...**

We pull the raw data from AWS S3 File storage to our AWS Redshift cluster and put the raw data into the staging tables. We then move the data from the staging tables into the respective Star Schema tables, the fact table is a combination of both files and the dimension tables grab additional information from the files as well.
> **Note:** The ETL logic is written in the file etl.py

## Files

**sql_queries.py**
This file contains all the queries that are used to CREATE, DROP, COPY, and INSERT the data into the tables. Each respective action is saved as an array of variables that are called in either the create_tables file or the ETL file.

**create_tables.py**
This file runs uses the variables inside of sql_queries to actually make the tables in the database and drop them if they already exist

**etl.py**
This file is where the ETL logic occurs, we grab the data files and pass them into their respective functions along with the connection to the database, the cursor, and the needed insert functions to fill the tables. In this file we get the data from the json files and then load it into the database

## How to run it (in the terminal)
**First:** create_tables.py must be ran first so that the relations exist in the database to be occupied. This file uses sql_queries.py
```
python create_tables.sql
```
**Second:** etl.py can then be ran which will extract the data from the files, transform it, then load it using sql_queries.py
```
python etl.py.sql
```
## AWS Documentation:
**S3**: The raw data exists in a public bucket in AWS S3, the data is stored in its raw JSON format and this is where we will need to access the data from to occupy our Data Warehouse

**RedShift**: This is the AWS DataWarehouse tool. We make a redshift cluster that we will be using to connect to our database, grab the data from S3, and fill the tables. This platform allows us to run our analytical queries and gain insight into the data.

**IAM**: Crate a Role that can have Read access to the S3 bucket, this lets us access the files from Redshift and perform the ETL.