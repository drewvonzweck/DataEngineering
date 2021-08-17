import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Description:
        Run all the queries that copy the data from S3 Bucket to the staging tables. These queries are in sql_queries.py
    
    Arguments: 
        cur: the cursor object
        conn: connection to the database in RedShift
        
    Returns:
        none
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Description:
        Run all the queries that insert the data from the Staging tables into the Star Schema table(Fact and Dimensions)
    
    Arguments: 
        cur: the cursor object
        conn: connection to the database in RedShift
        
    Returns:
        none
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Create config variable to hold the needed authentification variables for AWS
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Calls function to load data to staging tables  
    
    - Calls function to insert data from stagin tables to Fact and Dimension tables 
    
    - Finally, closes the connection. 
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()