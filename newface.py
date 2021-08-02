import csv
import cv2
import os
import time as tim
import psycopg2
import datetime
from os import path
import shutil
import train


def captureImage():
    
    input_id = input("Please enter you id: ")
    name = input("Please enter your name: ")

    user_exists = check_user_exists(input_id) # checks db if ID exists, returns int, used lated if face recognized

    if(user_exists == 0):      

        cam = cv2.VideoCapture(0) # Captures video from camera

        face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml') # Classifier for faces
        eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml') # Classifier for eyes
        sample_no = 0 # sample label for pictures to be gathered later
        rect_color = (0,0,255) # red


        # --- recognizer --- ##
        rec = cv2.face.LBPHFaceRecognizer_create()
        rec.read('labels' + os.sep + 'train.yml')
        # --- recognizer --- ##

        while cam.isOpened(): # While the camera is capturing
            ret, frame = cam.read() # read the camera and store each frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert feed to gray scale
            
            """
            scaleFactor determines how much the image is reduced (scaled)
            minNeighbors specifies how many neighbors each candidate rectangle should have to retain it. The higher the quality the less matches but the more accurate
        
            cv2.detectMultiScale returns the coordinates of the face area (x,y) + width,height of rectangle
            """
            faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5) # Detect face and convert it into grayscale

            for (x, y, w, h) in faces: 
                
                cv2.rectangle(frame, (x, y), (x + w, y + h), rect_color, 2) # draw rectangle around face
                
                region_gray = gray[y:y+h, x:x+w] # GrayScaled Face
                region_colored = frame[y:y+h, x:x+w] # Colored Face
                """
                Both are kept so the rectangle can be drawn on the live view photo and not the grayscaled 
                """
                
                # --- recognizer --- ##
                id, confidence = rec.predict(gray[y:y+h, x:x+w]) # Uses the gray face to analyise if face already exists. Returns the redicted id and confidence of result
                match_conf = round(100-confidence) # converts to %. The confidence returned has '1' as best value '100' as worst
                # --- recognizer --- ##

                # if the confidence is above 55 means the user is recognized and should not be re-registered with different credentials
                if match_conf > 55:
                   print("USER ALREADY EXISTS")
                   user_exists  = 1 # changes status, user now exists
                   break # avoid registery

                """
                Eye detection is used to ensure the validity of the face. If the eyes are not detected the system does not register the frame,
                as this has the change of it being faulty 
                """
                eyes = eye_cascade.detectMultiScale(region_gray, 1.5, 5) # detects eyes .detectMultiscale method is the same for faces

                for (ex, ey, ew, eh) in eyes:
                    
                    # middle of eye coordinates
                    midx = int(round((ex + (ex+ew)) / 2))
                    midy = int(round((ey + (ey+eh)) / 2))
                    cv2.rectangle(region_colored, (midx - 2, midy - 2), (midx + 2,midy + 2), rect_color) # draw recrangle in eyes

                    sample_no = sample_no + 1 # keeps track of images captured

                    training_dir = 'training' + os.sep # directory where to store images
                    mkdir_name =  training_dir + str(input_id) + '_' + name # directory name

                    #avoids error if it exists
                    if path.exists(mkdir_name) == False:
                        try:
                            os.mkdir(mkdir_name)     
                        except OSError as error:
                            print(error)
                            
                    cv2.imwrite(mkdir_name + os.sep + name + '_' + str(input_id) + '_' + str(sample_no) + '.png', region_gray) # Capture image

            cv2.imshow('frame', frame) # displays frame on cam window

            if cv2.waitKey(100) & 0xFF == ord('q') or user_exists == 1: # Wait 100s or escape key
                break
            elif sample_no > 100:
                break
        
        cam.release()
        cv2.destroyAllWindows()
        
        ##os.rmdir(mkdir_name)

        if user_exists != 1:
            add_new_user(input_id, name)

        else:
            if path.exists(mkdir_name):
                try:
                    shutil.rmtree(mkdir_name, ignore_errors=True) # delete directory with files
                except OSError as error:
                    print(error)
            
    else:
        print("Username already exists!")


def check_user_exists(input_id):
    # --- Connect to DataBase ---#
    existing_user = 0
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vba")

        cursor = connection.cursor() # cursor to execute command
        id_exists_query = f"SELECT * FROM users WHERE user_id = {input_id}" #query
        cursor.execute(id_exists_query) # execute query
        result = cursor.fetchall() # gets results

        if result:
            print("Employee already registered!")
            existing_user = 1
        else:
            print("Please look towards the camera")

    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
        existing_user = 1

    
    finally:
        connection.commit() # commits changes

        if connection:
            cursor.close()
            connection.close()

    return existing_user
    # --- Connect to DataBase ---#


def add_new_user(input_id, name):
    
    time_capture = tim.time() # capture current time
    user_register_capture = datetime.datetime.fromtimestamp(time_capture).strftime('%Y-%m-%d %H:%M:%S') # date in YYYY-MM-DD HH:MM:SS format

    json_data = {} # storage for all gathered data 

    json_data['user_id'] = str(input_id)
    json_data['user_name'] = name
    json_data['user_date_registered'] = user_register_capture

    #r = requests.post(url='http://127.0.0.1:5000/receive_data', json = json_data)
    #print("Status: ", r.status_code)

    try:
        # --- Connect to DataBase ---#
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vba")

        cursor = connection.cursor()

        insert_user_query = f"INSERT INTO users (user_id, user_name, user_date_registered) VALUES ('{json_data['user_id']}', '{json_data['user_name']}', '{json_data['user_date_registered']}')"
        cursor.execute(insert_user_query)               


    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)

    finally:
        connection.commit()

        if connection:
            cursor.close()
            connection.close()
    
    train_new_face()


def train_new_face():
    print("Teaching algorithm to detect the new face")
    train.trainFace()