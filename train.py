import os
import time
import cv2
import numpy as np
from PIL import Image
from threading import Thread
import click

def get_face_id(path):
    # imageLoc = [os.path.join(path, f) for f in os.listdir(path)] # joins 2 strings into a dir, if f is valid
    folders = [os.path.join(path, f) for f in os.listdir(path)] # joins 2 strings into a dir, if f is valid

    faces = [] # facest list
    ids = [] # id list

    #for img in imageLoc:
    for folder in folders:
        
        if folder == os.path.join(path, '.gitkeep'):
            continue
            
        imageLoc = [os.path.join(folder, f) for f in os.listdir(folder)] # joins 2 strings into a dir, if f is valid

        for img in imageLoc:

            if img == os.path.join(path, '.gitkeep'):
                continue

            pil_image = Image.open(img) # opens image in PIL format
            pil_image_gray = pil_image.convert('L') # converts it into grayscale

            image = np.array(pil_image, 'uint8') #converts PIL into array using the uint8 format
            
            test = os.path.split(img)
            user_folder = os.path.split(img)[0]
            details_split = user_folder.split('\\')[1]
            user_details_split = (details_split.split('_'))
            

            id = int(user_details_split[0])
            name = user_details_split[1]

            # id = int(os.path.split(img)[-1].split('_')[1]) # splits image name and gets id
            faces.append(image) # adds it to faces list
            # faces.append(cv2.resize(image,(480, 640)))
            ids.append(id) # adds to id list
        
    return faces, ids

def get_auto_id(path):
    imageLoc = [os.path.join(path, f) for f in os.listdir(path)] # joins 2 strings into a dir, if f is valid

    faces = [] # facest list
    ids = [] # id list

    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml') # Classifier for faces
    eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml') # Classifier for eyes
    sample_no = 0
    rect_color = (0,0,255)

    for img in imageLoc:

        if img == os.path.join(path, '.gitkeep'):
            continue

        # Open using CV2
        cap = cv2.VideoCapture(img)

        user_folder = os.path.split(img)[1]
        user_details_split = user_folder.split('_')

        id = int(user_details_split[0])
        name = user_details_split[1]


        while(cap.isOpened()):
            
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.5, 5) # Gray is the grayscaled frame, 1.3 is the scaleFactor, 0 are the minNeighbors and minsize is object size (not added)

            # cv2.imshow('frame',gray)

            for (x, y, w, h) in faces:
                
                # cv2.rectangle(frame, (x, y), (x + w, y + h), rect_color, 2)
                
                # separates the colored and gray face regions from the frame
                region_gray = gray[y:y+h, x:x+w] 
                region_colored = frame[y:y+h, x:x+w]

                eyes = eye_cascade.detectMultiScale(region_gray, 1.3, 5) # detects eyes

                for (ex, ey, ew, eh) in eyes:
                    
                    # middle of eye
                    # midx = round((ex + (ex+ew)) / 2)
                    # midy = round((ey + (ey+eh)) / 2)

                    # cv2.rectangle(region_colored, (midx - 2, midy - 2), (midx + 2,midy + 2), rect_color)
                    

                    sample_no = sample_no + 1 # keeps track of images captured
                
                    training_dir = 'training' + os.sep # directory where to store images
                    mkdir_name =  training_dir + str(id) + '_' + name # directory name

                    #avoids error if it exists
                    if os.path.exists(mkdir_name) == False:
                        try:
                            os.mkdir(mkdir_name)     
                        except OSError as error:
                            print(error)


                                        # Capture image
                    cv2.imwrite(mkdir_name + os.sep + name + '_' + str(id) + '_' +
                            str(sample_no) + '.png', region_gray)
                            

            if cv2.waitKey(1000) & 0xFF == ord('q'): # Wait 100s or escape key
                break
            elif sample_no > 20:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        os.remove(img)    



def trainFace():
    
    rec = cv2.face_LBPHFaceRecognizer.create() # creates recognizer using binary
    # rec = cv2.face_EigenFaceRecognizer.create() # creates regonizer using eignface
    #rec = cv2.face_FisherFaceRecognizer.create() # creates recognizer using fisherface 
    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml') # Classifier for faces
    
    get_auto_id('prerecorded')
    faces, id = get_face_id('training') # gets the face and labels from dir

    Thread(target = rec.train(faces, np.array(id))).start()

    print("Training Faces...")
    rec.save('labels' + os.sep + 'train.yml')    

    #fake loading bar
    # with click.progressbar(range(10000000)) as bar:
    #     for i in bar:
    #         pass 