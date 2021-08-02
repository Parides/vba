import psycopg2
import configparser

config = configparser.ConfigParser() # initialization of configparser.
config.read('config.ini') # config read

def connect_to_db():
    try:
        connection = psycopg2.connect(  user = config['PostgreSQL']['user'], 
                                        password = config['PostgreSQL']['pass'], 
                                        host = config['PostgreSQL']['host'], 
                                        database = config['PostgreSQL']['db'])

    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)

    finally:
       return connection



def fetch_data(connection, query):

    try:
        cursor = connection.cursor() # opens a cursor which allows query execution
        cursor.execute(query) # execute parsed query

        result = cursor.fetchall() # fetch data returned from query

        if result: # if data fetched
            return result 
        else:
            return 0 # 0 to denote NULL

    except (Exception, psycopg2.DatabaseError) as error:
        return 0  # 0 to denote NULL
        print("ERROR DB: ", error)

    finally:
        connection.commit()
        cursor.close() # terminates cursor
        connection.close() # terminates database connection




def insert_or_delete(connection, query):
    try:
        cursor = connection.cursor() # opens a cursor which allows query execution
        cursor.execute(query) # execute parsed query
        
    except (Exception, psycopg2.DatabaseError) as error:
        return 0  # 0 to denote NULL
        print("ERROR DB: ", error)

    finally:
        connection.commit() # commits changes
        cursor.close() # terminates cursor
        connection.close() # terminates database connection

    return 1 # if executed successfully 