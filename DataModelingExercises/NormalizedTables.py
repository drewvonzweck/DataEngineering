#!/usr/bin/env python
# coding: utf-8

# # Lesson 2 Exercise 1: Creating Normalized Tables



import psycopg2


# ####  Create a connection to the database, get a cursor, and set autocommit to true

# In[2]:


try: 
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
except psycopg2.Error as e: 
    print("Error: Could not make connection to the Postgres database")
    print(e)
try: 
    cur = conn.cursor()
except psycopg2.Error as e: 
    print("Error: Could not get cursor to the Database")
    print(e)
conn.set_session(autocommit=True)


# #### Let's imagine we have a table called Music Store. 
# 
# `Table Name: music_store
# column 0: Transaction Id
# column 1: Customer Name
# column 2: Cashier Name
# column 3: Year 
# column 4: Albums Purchased`
# 
# ## Now to translate this information into a Create Table Statement and insert the data
# 
# 
# <img src="images/table12.png" width="650" height="650">
# 

# In[3]:


# We Create Table Statement and insert the data in the table
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS music_store (transaction_id int,                                                          customer_name varchar, cashier_name varchar,                                                          year int, albums_purchased text[]);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store (transaction_id, customer_name, cashier_name, year, albums_purchased)                  VALUES (%s, %s, %s, %s, %s)",                  (1, "Amanda", "Sam", 2000, ["Rubber Soul", "Let it Be"]))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store (transaction_id, customer_name, cashier_name, year, albums_purchased)                  VALUES (%s, %s, %s, %s, %s)",                  (2, "Toby", "Sam", 2000, ["My Generation"]))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store (transaction_id, customer_name, cashier_name, year, albums_purchased)                  VALUES (%s, %s, %s, %s, %s)",                  (3, "Max", "Bob", 2018, ["Meet the Beatles", "Help!"]))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
    
try: 
    cur.execute("SELECT * FROM music_store;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


# #### Moving to 1st Normal Form (1NF)
# This data has not been normalized. To get this data into 1st normal form, we will need to remove any collections or list of data. We need to break up the list of songs into individual rows. 
# 
# `Table Name: music_store
# column 0: Transaction Id
# column 1: Customer Name
# column 2: Cashier Name
# column 3: Year 
# column 4: Albums Purchased`
# 
# <img src="images/table13.png" width="650" height="650">

# In[4]:


try: 
    cur.execute("CREATE TABLE IF NOT EXISTS music_store2 (transaction_id int,                                                          customer_name varchar, cashier_name varchar,                                                          year int, albums_purchased text);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store2 (transaction_id, customer_name, cashier_name, year, albums_purchased)                  VALUES (%s, %s, %s, %s, %s)",                  (1, "Amanda", "Sam", 2000, "Rubber Soul"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO music_store2 (transaction_id, customer_name, cashier_name, year, albums_purchased)                  VALUES (%s, %s, %s, %s, %s)",                  (1, "Amanda", "Sam", 2000, "Let it Be"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store2 (transaction_id, customer_name, cashier_name, year, albums_purchased)                  VALUES (%s, %s, %s, %s, %s)",                  (2, "Toby", "Sam", 2000, "My Generation"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store2 (transaction_id, customer_name, cashier_name, year, albums_purchased)                  VALUES (%s, %s, %s, %s, %s)",                  (3, "Max", "Bob", 2018, "Help!"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store2 (transaction_id, customer_name, cashier_name, year, albums_purchased)                  VALUES (%s, %s, %s, %s, %s)",                  (3, "Max", "Bob", 2018, "Meet the Beatles"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("SELECT * FROM music_store2;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


# #### Moving to 2nd Normal Form (2NF)
# We have moved our data to be in 1NF which is the first step in moving to 2nd Normal Form. Our table is not yet in 2nd Normal Form. While each of our records in our table is unique, our Primary key (transaction id) is not unique. We need to break this up into two tables, transactions and albums sold. 
# 
# `Table Name: transactions 
# column 0: Transaction ID
# column 1: Customer Name
# column 2: Cashier Name
# column 3: Year `
# 
# `Table Name: albums_sold
# column 0: Album Id
# column 1: Transaction Id
# column 3: Album Name` 
# 
# <img src="images/table14.png" width="450" height="450"> <img src="images/table15.png" width="450" height="450">

# In[5]:


# We create two new tables transactions and albums sold and insert data into these tables

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS transactions (transaction_id int,                                                            customer_name varchar, cashier_name varchar,                                                            year int);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS albums_sold (album_id int, transaction_id int,                                                           album_name varchar);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute("INSERT INTO transactions (transaction_id, customer_name, cashier_name, year)                  VALUES (%s, %s, %s, %s)",                  (1, "Amanda", "Sam", 2000))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO transactions (transaction_id, customer_name, cashier_name, year)                  VALUES (%s, %s, %s, %s)",                  (2, "Toby", "Sam", 2000))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO transactions (transaction_id, customer_name, cashier_name, year)                  VALUES (%s, %s, %s, %s)",                  (3, "Max", "Bob", 2018))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO albums_sold (album_id, transaction_id, album_name)                  VALUES (%s, %s, %s)",                  (1, 1, "Rubber Soul"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO albums_sold (album_id, transaction_id, album_name)                  VALUES (%s, %s, %s)",                  (2, 1, "Let it Be"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO albums_sold (album_id, transaction_id, album_name)                  VALUES (%s, %s, %s)",                  (3, 2, "My Generation"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO albums_sold (album_id, transaction_id, album_name)                  VALUES (%s, %s, %s)",                  (4, 3, "Meet the Beatles"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO albums_sold (album_id, transaction_id, album_name)                  VALUES (%s, %s, %s)",                  (5, 3, "Help!"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

print("Table: transactions\n")
try: 
    cur.execute("SELECT * FROM transactions;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

print("\nTable: albums_sold\n")
try: 
    cur.execute("SELECT * FROM albums_sold;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)
row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


# #### Let's do a `JOIN` on this table so we can get all the information we had in our first Table. 

# In[6]:


# We complete the join on the transactions and album_sold tables

try: 
    cur.execute("SELECT * FROM transactions JOIN albums_sold ON transactions.transaction_id = albums_sold.transaction_id ;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


# #### Moving to 3rd Normal Form (3NF)
# Let's check our table for any transitive dependencies. Transactions can remove Cashier Name to its own table, called Employees, which will leave us with 3 tables. 
# `Table Name: transactions2 
# column 0: transaction Id
# column 1: Customer Name
# column 2: Cashier Id
# column 3: Year `
# 
# `Table Name: albums_sold
# column 0: Album Id
# column 1: Transaction Id
# column 3: Album Name` 
# 
# `Table Name: employees
# column 0: Employee Id
# column 1: Employee Name `
# <img src="images/table16.png" width="450" height="450"> <img src="images/table15.png" width="450" height="450"> <img src="images/table17.png" width="350" height="350">
# 

# In[7]:


try: 
    cur.execute("CREATE TABLE IF NOT EXISTS transactions2 (transaction_id int,                                                            customer_name varchar, cashier_id int,                                                            year int);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS employees (employee_id int,                                                        employee_name varchar);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

try: 
    cur.execute("INSERT INTO transactions2 (transaction_id, customer_name, cashier_id, year)                  VALUES (%s, %s, %s, %s)",                  (1, "Amanda", 1, 2000))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO transactions2 (transaction_id, customer_name, cashier_id, year)                  VALUES (%s, %s, %s, %s)",                  (2, "Toby", 1, 2000))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO transactions2 (transaction_id, customer_name, cashier_id, year)                  VALUES (%s, %s, %s, %s)",                  (3, "Max", 2, 2018))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO employees (employee_id, employee_name)                  VALUES (%s, %s)",                  (1, "Sam"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO employees (employee_id, employee_name)                  VALUES (%s, %s)",                  (2, "Bob"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)    

print("Table: transactions2\n")
try: 
    cur.execute("SELECT * FROM transactions2;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

print("\nTable: albums_sold\n")
try: 
    cur.execute("SELECT * FROM albums_sold;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

print("\nTable: employees\n")
try: 
    cur.execute("SELECT * FROM employees;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


# #### Let's do two `JOIN` on these 3 tables so we can get all the information we had in our first Table. 

# In[8]:


try: 
    cur.execute("SELECT * FROM (transactions2 JOIN albums_sold ON                                transactions2.transaction_id = albums_sold.transaction_id) JOIN                                employees ON transactions2.cashier_id=employees.employee_id;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


# ### DONE! We have Normalized our dataset! 

# ### For the sake of the demo, Iet's drop the tables. 

# In[9]:


try: 
    cur.execute("DROP table music_store")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table music_store2")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table albums_sold")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table employees")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table transactions")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table transactions2")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)


# ### And finally close the cursor and connection. 

# In[10]:


cur.close()
conn.close()


# In[ ]:




