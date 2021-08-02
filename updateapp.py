import psycopg2
import train, removeuser
from tkinter import simpledialog
import datetime
import time as tim
import connections
import os

def gather_existing_ids():
    query = "SELECT user_id FROM users WHERE permissions_id = 3 and user_biometric_consent = 'False'"
    result = connections.fetch_data(connection=connections.connect_to_db(), query = query)

    if result:
        result_new = []
        for row in result:
            result_new.append(row[0])
        return result_new
    else:
        result = []
        return result

def yml_ids():
    faces, ids = train.get_face_id('training')
    unique_ids = []
    for id in ids:
        if id in unique_ids:
            continue
        else:
            unique_ids.append(str(id))
    return unique_ids

def cross_check():
    db_ids = gather_existing_ids()
    trained_ids = yml_ids()

    for ids in db_ids:
        if ids in trained_ids:
            # remove_pictures
            print('\033[91m' + "ID has biometrics disabled")
            print('\033[91m' + "Removing data from trainer")
        else:
            print(1)

#1 Gather all existing database ID's -- Done
#2 Check if they exist in the YML
#3 If they dont exist in the database 

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
    


def check_user_input():
    info = {}

    module_codes = get_module_codes()

    while True:  
        info['module_code'] = simpledialog.askstring(title="Module Code", prompt="What's the module code?")

        if info['module_code'] in module_codes:
            password = simpledialog.askstring(title="Enter Module Password", prompt="Please enter the modules admin password")
            break
        elif info['module_code'] == None:
            return

    info['week_number'] = simpledialog.askstring(title="Week Number", prompt="What week are we on?")
    if info['week_number'] == None:
        return
    
    info['session_name']= simpledialog.askstring(title="Session Name", prompt="What your session name?")
    if info['session_name'] == None:
        return


    create_session(info)

    return info


def get_module_codes():
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        cursor = connection.cursor() # cursor to execute command
        all_module_ids = f"SELECT module_id FROM modules"
        cursor.execute(all_module_ids)
        result = cursor.fetchall() # gets results

        if result:
            data =[]

            for row in result:
                data.append(row[0])

    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
    
    finally:
        connection.commit() # commits changes

        if connection:
            cursor.close()
            connection.close()

        return data
        # --- Connect to DataBase ---#


def create_session(session_info):
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        moduel_code = session_info['module_code']
        week_number = session_info['week_number'] 
        session_name = session_info['session_name']
        session_full_description = 'Week '+ week_number + ' ' + session_name
        time_capture = tim.time() # capture current time
        current_date = datetime.datetime.fromtimestamp(time_capture).strftime('%Y-%m-%d') # date in YYYY-MM-DD HH:MM:SS format
        current_timestamp = datetime.datetime.fromtimestamp(time_capture).strftime("%Y-%m-%d %H:%M:%S")


        cursor = connection.cursor() # cursor to execute command
        all_module_ids = f"SELECT * FROM module_sessions WHERE session_date::text LIKE '{current_date}%' AND module_id = '{moduel_code}' AND session_name = '{session_name}'"
        cursor.execute(all_module_ids)
        result = cursor.fetchall() # gets results

        if result:
            print(1)

        else:
            add_new_session = f"INSERT INTO public.module_sessions(module_id, session_date, session_name) VALUES ('{moduel_code}', '{current_timestamp}','{session_full_description}');"
            cursor.execute(add_new_session)

    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
    
    finally:
        connection.commit() # commits changes

        if connection:
            cursor.close()
            connection.close()

        return print(':)')
        # --- Connect to DataBase ---#
