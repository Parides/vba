import cv2

def camtest():
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) # Captures video from camera

    while cap.isOpened(): # While the camera is capturing

        ret, frame = cap.read() # Captures frames (30fps)
        
        cv2.imshow('Camera feed', frame) # Displays the feed

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
        
    # return_value, image = camera.read()
    # cv2.imwrite("image.png",)