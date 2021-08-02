import cv2

def facedetect():
    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml') # Classifier for faces
    eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml') # Classifier for eyes
    smile_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_smile.xml') # Classifier for eyes

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) # Captures video from camera

    while cap.isOpened(): # While the camera is capturing

        ret, frame = cap.read() # Captures frames (30fps)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Converts feed to gray scale

        # Detect Face
        faces = face_cascade.detectMultiScale(gray, 1.5 , 5)
        #faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30,30), flags = cv2.CASCADE_SCALE_IMAGE)

        rect_color = (0,0,255)
        # Draw Rectangle around the face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), rect_color, 2)

            face_area = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(face_area, 1.3, 5)
            for (ex, ey, ew, eh) in eyes:
                midx = int(round((ex + (ex+ew)) / 2))
                midy = int(round((ey + (ey+eh)) / 2))

                # cv2.rectangle(roi_color, (midx, midy), (midx,midy), rect_color)
                cv2.rectangle(roi_color, (midx - 2, midy - 2), (midx + 2,midy + 2), rect_color)
                # cv2.circle(roi_color, (midx,midy), 6, rect_color)
            # (from where, )
            # smiles =  smile_cascade.detectMultiScale(face_area, 1.3, 5)
            # for(sx, sy, sw, sh) in smiles:
            #     cv2.rectangle(roi_color, (ex, sy), (sx+sw, sy+sh), rect_color)

        cv2.imshow('Camera feed', frame) # Displays the feed

        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()
    # return_value, image = camera.read()
    # cv2.imwrite("image.png",)