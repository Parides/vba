import psycopg2
import os
from os import path
import shutil

def remove_user_btn():
    input_id = input("Please enter ID: ")

    remove_user(input_id)


def remove_user(input_id):
  
# --- Connect to DataBase ---#
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vba")

        cursor = connection.cursor() # cursor to execute command
        # id_exists_query = f"SELECT * FROM users WHERE user_id = {input_id}" #query
        user_delete_query = f"DELETE FROM users WHERE user_id = {input_id}" # query
        result = cursor.execute(user_delete_query) # execute query
        # result = cursor.fetchall() # gets results

    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)

    
    finally:
        connection.commit() # commits changes
        print("User with ID: ", input_id, " has been removed from the database")
        print("Removing Pictures...")
        remove_pictures(input_id)
        
        if connection:
            cursor.close()
            connection.close()
    # --- Connect to DataBase ---#

def remove_pictures(input_id):
    path_ = 'training'
    imageLoc = [os.path.join(path_, f) for f in os.listdir(path_)] # joins 2 strings into a dir, if f is valid

    ids = []
    for img in imageLoc:

        if img == os.path.join(path_, '.gitkeep'):
            continue

        id = os.path.split(img)[-1].split('_')[0] # splits image name and gets id
        #ids.append(id)

        if id == input_id:
            if path.exists(img):
                try:
                    shutil.rmtree(img, ignore_errors=True) # delete directory with files
                except OSError as error:
                    print(error)
#def remove_db_data():