#!/usr/bin/env python
# coding: utf-8

# # Lesson 1 Exercise 1: Creating a Table with PostgreSQL
# 
# <img src="images/postgresSQLlogo.png" width="250" height="250">

# ### Walk through the basics of PostgreSQL. You will need to complete the following tasks:<li> Create a table in PostgreSQL, <li> Insert rows of data <li> Run a simple SQL query to validate the information. <br>
# `#####` denotes where the code needs to be completed. 
#     
# Note: __Do not__ click the blue Preview button in the lower task bar

# #### Import the library 
# *Note:* An error might popup after this command has executed. If it does, read it carefully before ignoring. 

# In[46]:


import psycopg2


# In[47]:


get_ipython().system('echo "alter user student createdb;" | sudo -u postgres psql')


# ### Create a connection to the database

# In[59]:


try: 
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
except psycopg2.Error as e: 
    print("Error: Could not make connection to the Postgres database")
    print(e)


# ### Use the connection to get a cursor that can be used to execute queries.

# In[60]:


try: 
    cur = conn.cursor()
except psycopg2.Error as e: 
    print("Error: Could not get curser to the Database")
    print(e)


# ### TO-DO: Set automatic commit to be true so that each action is committed without having to call conn.commit() after each command. 

# In[61]:


conn.set_session(autocommit=True)


# ### TO-DO: Create a database to do the work in. 

# In[62]:


## TO-DO: Add the database name within the CREATE DATABASE statement. You can choose your own db name.
try: 
    cur.execute("create database newbase")
except psycopg2.Error as e:
    print(e)


# #### TO-DO: Add the database name in the connect statement. Let's close our connection to the default database, reconnect to the Udacity database, and get a new cursor.

# In[63]:


## TO-DO: Add the database name within the connect statement
try: 
    conn.close()
except psycopg2.Error as e:
    print(e)
    
try: 
    conn = psycopg2.connect("host=127.0.0.1 dbname=newbase user=student password=student")
except psycopg2.Error as e: 
    print("Error: Could not make connection to the Postgres database")
    print(e)
    
try: 
    cur = conn.cursor()
except psycopg2.Error as e: 
    print("Error: Could not get curser to the Database")
    print(e)

conn.set_session(autocommit=True)


# ### Create a Song Library that contains a list of songs, including the song name, artist name, year, album it was from, and if it was a single. 
# 
# `song_title
# artist_name
# year
# album_name
# single`
# 

# In[64]:


## TO-DO: Finish writing the CREATE TABLE statement with the correct arguments
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS songlibrary (song_title VARCHAR(30), artist_name VARCHAR(30), year INTEGER, album_name VARCHAR(30), single BOOLEAN);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)


# ### TO-DO: Insert the following two rows in the table
# `First Row:  "Across The Universe", "The Beatles", "1970", "False", "Let It Be"`
# 
# `Second Row: "The Beatles", "Think For Yourself", "False", "1965", "Rubber Soul"`

# In[65]:


## TO-DO: Finish the INSERT INTO statement with the correct arguments

try: 
    cur.execute("INSERT INTO songlibrary (song_title,artist_name,year,single,album_name)                  VALUES (%s, %s, %s, %s, %s)",                  ("Across The Universe", "The Beatles", "1970", "False", "Let It Be"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO songlibrary (artist_name,song_title,single,year,album_name)                   VALUES (%s, %s, %s, %s, %s)",
                  ("The Beatles", "Think For Yourself", "False", "1965", "Rubber Soul"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)


# ### TO-DO: Validate your data was inserted into the table. 
# 

# In[ ]:





# In[57]:


## TO-DO: Finish the SELECT * Statement 
try: 
    cur.execute("SELECT * FROM songlibrary;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


# ### And finally close your cursor and connection. 

# In[58]:


cur.close()
conn.close()


# In[ ]:




