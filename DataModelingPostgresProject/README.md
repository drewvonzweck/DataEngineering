# PROJECT 1: DATA MODELING POSTGRES

## WHAT IS SPARKIFY?

**This database if for a start up called Sparkify**, which is a music streaming application. They wish to better understand what songs their users are listening to. For this we needs to organize their files and sloppy data into a database.
The identified tables are...

## TABLES:

### FACT TABLE
**songplays** - records in log data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### DIMENSION TABLES

**users** - users in the app
user_id, first_name, last_name, gender, level

**songs** - songs in music database
song_id, title, artist_id, year, duration

**artists** - artists in music database
artist_id, name, location, latitude, longitude

**time** - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday

> **Note:** These tables are in a Star Schema and provide a clear division of entities and give the ability to split the given data sets into a logical set of relations

## DATA:

**log_data:** a collection of Json files that log the users interacting with the application.

ex: {"artist":"The Grass Roots","auth":"Logged In","firstName":"Sara","gender":"F","itemInSession":72,"lastName":"Johnson","length":166.71302,"level":"paid","location":"Winston-Salem, NC","method":"PUT","page":"NextSong","registration":1540809153796.0,"sessionId":411,"song":"Let's Live For Today","status":200,"ts":1542153802796,"userAgent":"\"Mozilla\/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit\/537.51.2 (KHTML, like Gecko) Version\/7.0 Mobile\/11D257 Safari\/9537.53\"","userId":"95"}

**song_data**: a collection of song data that has important attributes for the songs. In JSON format

ex:{"num_songs": 1, "artist_id": "ARGCY1Y1187B9A4FA5", "artist_latitude": 36.16778, "artist_longitude": -86.77836, "artist_location": "Nashville, TN.", "artist_name": "Gloriana", "song_id": "SOQOTLQ12AB01868D0", "title": "Clementina Santaf\u00e8", "duration": 153.33832, "year": 0}

## ETL:
 
**The ETL works as so...**

Pull the data out of the files that contain the json data
Put this data into a dataframe where we can select the appropriate attributes
Clean up this data and make sure the attributes are in the proper format
Load this data into the appropriate table from our star schema
> **Note:** The ETL logic is written in the file etl.py

## Files

**sql_queries.py**
In this file the statements for CREATE, INSERT, and SELECT are stored in variables to be passed to create_tables.py and etl.py

**create_tables.py**
This file runs uses the variables holding the CREATE statments to run actually make the tables in the database and drop them if they already exist

**etl.py**
This file is where the ETL logic occurs, we grab the data files and pass them into their respective functions along with the connection to the database, the cursor, and the needed insert functions to fill the tables. In this file we get the data from the json files, transform it using the pandas libray, and then load it into the database

## How to run it (in the terminal)
**First:** create_tables.py must be ran first so that the relations exist in the database to be occupied. This file uses sql_queries.py
```
python create_tables.py
```
**Second:** etl.py can then be ran which will extract the data from the files, transform it, then load it using sql_queries.py
```
python etl.py
