from datetime import datetime
import os
import time as tim
import cv2
import pandas as pd
import psycopg2
from PIL import ImageGrab
import numpy as np
import updateapp



def recognize(session_info):

    rec = cv2.face.LBPHFaceRecognizer_create() # creates a face recognition classifier
    # rec = cv2.face.EigenFaceRecognizer_create() # creates a face recognition classifier
    #rec = cv2.face.FisherFaceRecognizer_create() # creates a face recognition classifier

    rec.read('labels' + os.sep + 'train.yml') # uses the trained data from the yml file

    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml') # Classifier for faces

    updateapp.create_session(session_info) # new session
    existing_users = get_users(session_info['module_code']) # gets existing users in db
    
    font = cv2.FONT_HERSHEY_PLAIN # sets font 

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #CAP_DSHOW is video input
    cam.set(3, 640)
    cam.set(4, 480)

    min_face_w = 0.1 * cam.get(3)
    min_face_h = 0.1 * cam.get(4)

    rect_color = (0,0,255)
    red =  (0,0,255)
    green = (0,255,0)
    blue = (255,0,0)


    while cam.isOpened():

        ret, frame = cam.read() # read the camera and store each frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert feed to gray scale

        """
        scaleFactor determines how much the image is reduced (scaled)
        minNeighbors specifies how many neighbors each candidate rectangle should have to retain it. The higher the quality the less matches but the more accurate

        cv2.detectMultiScale returns the coordinates of the face area (x,y) + width,height of rectangle
        """
        faces = face_cascade.detectMultiScale(gray, 1.2, 5,minSize = (int(min_face_w), int(min_face_w)),flags = cv2.CASCADE_SCALE_IMAGE) # Detect face and convert it into grayscale


        for(x, y, w, h) in faces:
            
            # cv2.rectangle(frame, (x, y), (x + w, y + h), rect_color, 2)
            
            # --- recognizer --- ##
            # gray = gray[y:y+h, x:x+w]
            # gray = cv2.resize(gray, (480, 640))
            # id,confidence = rec.predict(gray)
            id, confidence = rec.predict(gray[y:y+h, x:x+w])  # Uses the gray face to analyise if face already exists. Returns the redicted id and confidence of result
            match_conf = round(100-confidence) # converts to %. The confidence returned has '1' as best value '100' as worst
            # --- recognizer --- ##

            match_perc = ' ' + str(round(100-confidence)) + '%'
            
            if match_conf > 55:
                
                display_string, name = get_display_string(match_conf, id, existing_users)

                # --- Log Data --- # 

                time_capture = tim.time() # captures timestamp
                timestamp = datetime.fromtimestamp(time_capture).strftime('%Y-%m-%d %H:%M:%S') # date in YYYY-MM-DD format
                date = datetime.fromtimestamp(time_capture).strftime('%Y-%m-%d') # date in YYYY-MM-DD format
                time = datetime.fromtimestamp(time_capture).strftime('%H:%M:%S') # time in HH:MM:SS

                data = {}

                data['id'] = str(id)
                data['name'] = name
                data['date'] = date
                data['time'] = time
                # --- Log Data --- # 
                
                if str(id) in existing_users:
                    logged = log_to_db(data, gray[y:y+h, x:x+w], session_info)
            
            elif match_conf > 40:

                display_string, name = get_display_string(match_conf, id, existing_users)

            else:
                display_string, name = get_display_string(match_conf, id, existing_users)
               
                
            cv2.putText(frame, str(display_string), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        
            
            if match_conf > 55:
                cv2.putText(frame, str(match_perc), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
                cv2.rectangle(frame, (x, y), (x + w, y + h), green, 2)
            
            elif match_conf > 40:
                cv2.putText(frame, str(match_perc), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), blue, 2)

            else:
                cv2.putText(frame, str(match_perc), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), red, 2)


        cv2.imshow('Attendance', frame)

        
        if cv2.waitKey(1) == 27: #ESC
            break
        
    cam.release()
    cv2.destroyAllWindows()


def get_users(module_id):
    # -- read users from db -- #
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        cursor = connection.cursor() # cursor to execute command
        
        module_users = f"SELECT users_modules.user_id, user_name FROM users_modules RIGHT JOIN users ON users_modules.user_id = users.user_id WHERE users_modules.module_id = '{module_id}' and users.user_biometric_consent = 'True'"

        cursor.execute(module_users)
        result = cursor.fetchall() # gets the results

        if result:
            existing_users = {} # storage for the existing users in the database

            for row in result:
                name = row[1]
                id = row[0]
                existing_users[id] = {'name' : name}
            
        else:
            print("No users registered in the system")      
            existing_users = {} 
            
    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
    
    finally:
        connection.commit()
        if connection:
            cursor.close()
            connection.close()

    return existing_users
    # -- read users from db -- #


def log_to_db(data, face, session_info):

    logged = 0

    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")
       
        cursor = connection.cursor()        
        time_capture = tim.time() # capture current time
        current_date = datetime.fromtimestamp(time_capture).strftime('%Y-%m-%d') # date in YYYY-MM-DD HH:MM:SS format
        current_timestamp = datetime.fromtimestamp(time_capture).strftime("%Y-%m-%d %H:%M:%S")

        get_session_id = f"SELECT session_id FROM module_sessions WHERE session_date::text LIKE '{current_date}%' AND module_id = '{session_info['module_code']}' AND session_name LIKE'%{session_info['session_name']}'"
        cursor.execute(get_session_id)
        current_session_id = cursor.fetchall()[0][0] # gets results

        if current_session_id:
            #print("identified already")
            has_been_seen_quert = f"SELECT * FROM attendance WHERE session_id = '{current_session_id}' AND user_id = '{data['id']}'"
            cursor.execute(has_been_seen_quert)
            result = cursor.fetchall() # gets results

            if result:
                logged = 0
            else:
                logged = 1
                img_loc = 'captures' + os.sep + data['id'] + "_" + str(current_session_id) + '_' + current_timestamp + '.png' # capture save location
                insert_attendance = f"INSERT INTO public.attendance(module_id, session_id, user_id, attendance_time, attendance_capture) VALUES ('{session_info['module_code']}', '{current_session_id}', '{data['id']}', '{current_timestamp}', '{img_loc}');"
                cursor.execute(insert_attendance)
        # else:
        #     logged = 1
            
        #     # insert_user_query = f"INSERT INTO attendance (id, name, date, time) VALUES ('{json_data['id']}', '{json_data['name']}', '{json_data['date']}', '{json_data['time']}')"
        #     insert_user_query = f"INSERT INTO session (user_id, session_date, session_time, img_loc) VALUES ('{data['id']}', '{data['date']}','{data['time']}','{img_loc}')"

        #     cursor.execute(insert_user_query)   
        else:
            print("something went wrong")
            
    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)

    
    finally:
        connection.commit()
        
        if connection:
            cursor.close()
            connection.close()

    if logged == 1:
        cv2.imwrite(img_loc, face) # capture snapshot
        return logged,img_loc
    else:
        return logged
    

def get_display_string(match_conf, id, existing_users):
    
    display_string = None
    match_name = None
    id = str(id)

    if id in existing_users:

        if match_conf > 55:
            match_name = existing_users[id]['name'] # gets name relative to database id
            match_sign = ' [LOGGED] ' # identification status
        
        elif match_conf > 40:
            match_name = existing_users[id]['name'] # gets name relative to database id
            match_sign = ' [UNSURE] ' # identification status
        
        else:
            id = ""
            match_name = ""
            match_sign = ' [UNKNOWN] '

    else:

        match_name = ""
        match_sign = ' [UNREGISTERED] '

    display_string = str(id) + ' - ' + str(match_name) + match_sign

    return display_string, match_name



def recognize_feed(session_info):

    rec = cv2.face.LBPHFaceRecognizer_create() # creates a face recognition classifier
    rec.read('labels' + os.sep + 'train.yml') # uses the trained data from the yml file

    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml') # Classifier for faces

    updateapp.create_session(session_info) # new session
    existing_users = get_users(session_info['module_code']) # gets existing users in db


    font = cv2.FONT_HERSHEY_PLAIN # sets font 


    rect_color = (0,0,255)
    red =  (0,0,255)
    green = (0,255,0)
    blue = (255,0,0)



    fourcc = cv2.VideoWriter_fourcc(*'MPV4')
    #out = cv2.VideoWriter("output.mp4", fourcc, 5.0, (1920,1080))


    while True:
            
        snapshot = ImageGrab.grab()
        snapshot_np = np.array(snapshot)

        frame = cv2.cvtColor(snapshot_np, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(snapshot_np, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.2, 5,flags = cv2.CASCADE_SCALE_IMAGE) # Detect face and convert it into grayscale
        
        for(x, y, w, h) in faces:
            
            # cv2.rectangle(frame, (x, y), (x + w, y + h), rect_color, 2)
            
            # --- recognizer --- ##
            id, confidence = rec.predict(gray[y:y+h, x:x+w])  # Uses the gray face to analyise if face already exists. Returns the redicted id and confidence of result
            match_conf = round(100-confidence) # converts to %. The confidence returned has '1' as best value '100' as worst
            # --- recognizer --- ##

            match_perc = ' ' + str(round(100-confidence)) + '%'
            
            if match_conf > 55:
                
                display_string, name = get_display_string(match_conf, id, existing_users)

                # --- Log Data --- # 

                time_capture = tim.time() # captures timestamp
                timestamp = datetime.fromtimestamp(time_capture).strftime('%Y-%m-%d %H:%M:%S') # date in YYYY-MM-DD format
                date = datetime.fromtimestamp(time_capture).strftime('%Y-%m-%d') # date in YYYY-MM-DD format
                time = datetime.fromtimestamp(time_capture).strftime('%H:%M:%S') # time in HH:MM:SS

                data = {}

                data['id'] = str(id)
                data['name'] = name
                data['date'] = date
                data['time'] = time
                # --- Log Data --- # 
                
                if id in existing_users:
                    logged = log_to_db(data, gray[y:y+h, x:x+w],session_info)
            
            elif match_conf > 40:

                display_string, name = get_display_string(match_conf, id, existing_users)

            else:
                display_string, name = get_display_string(match_conf, id, existing_users)
               
                
            cv2.putText(frame, str(display_string), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        
            
            if match_conf > 55:
                cv2.putText(frame, str(match_perc), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
                cv2.rectangle(frame, (x, y), (x + w, y + h), green, 2)
            
            elif match_conf > 40:
                cv2.putText(frame, str(match_perc), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), blue, 2)

            else:
                cv2.putText(frame, str(match_perc), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), red, 2)


        resized = cv2.resize(frame, (960, 540))
        cv2.imshow("Screen", resized)
        #out.write(frame)


        

        if cv2.waitKey(1) == 27: #ESC
            break

    #out.release()
    cv2.destroyAllWindows()