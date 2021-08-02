import tkinter as tk
from tkinter import *
from tkinter import ttk
import test, camtest, newface, recognize, train, removeuser,updateapp
from tkinter import simpledialog
from ttkthemes import themed_tk
import tkinter.messagebox

# ------------- Starting Functions ------------- # 
# train.trainFace()
#updateapp.gather_existing_ids()
#updateapp.yml_ids()
# updateapp.cross_check()
#removeuser.remove_pictures()

train.trainFace()
e = updateapp.gather_existing_ids()
updateapp.cross_check()
def start():
    # ------------- Window ------------- # 
    window = themed_tk.ThemedTk() # lets up the window
    window.get_themes()
    window.set_theme('breeze')
    window.title('Vision Based Attendance Analyzer') # window title
    window.iconbitmap(r'favicon.ico')
    window.geometry('800x600') # window res


    # ------------- Menu Bar ------------- # 
    menubar = Menu(window)
    window.config(menu = menubar)

    def about_us():
        tkinter.messagebox.showinfo('Help', 'How to use:\n1. Test')


    submenu = Menu(menubar, tearoff = 0)
    menubar.add_cascade(label="File", menu = submenu)
    submenu.add_radiobutton(label = 'Help', command = about_us)
    submenu.add_command(label = 'Exit', command = window.destroy)





    # ------------- Tabs ------------- # 
    tabs = ttk.Notebook(window) # sets up tab section ontop of window

    tab1 = ttk.Frame(tabs) # tab1
    tabs.add(tab1, text='Attendance')

    tab2 = ttk.Frame(tabs)
    tabs.add(tab2, text='Analysis')


    # ------------- Methods ------------- # 
    def detect():
        test.facedetect()

    def testcamera():
        camtest.camtest()

    def regnew():
        newface.captureImage()

    def trainSys():
        train.trainFace()

    def recFace():
        session_info = updateapp.check_user_input()
        if session_info != None:
            recognize.recognize(session_info)

    def recFeed():
        session_info = updateapp.check_user_input()
        if session_info != None:
            recognize.recognize_feed(session_info)

    def removeUser():
        removeuser.remove_user_btn()

    def exit_program():
        exit()
    # ------------- Tab1 ------------- # 

    # --- Widgets --- #
    tab1_title = tk.Label(tab1, text = 'Attendance Analyzer')

    rec = PhotoImage(file='C:\\Users\\antre\\Desktop\\Year 3\\CS3IP16\\vision-based-attendance-analyser\\static\\rec.png')
    camtest_btn = tk.Button(tab1, text = "OMEGALUL", image = rec,  command = testcamera)
    register_btn = tk.Button(tab1, text= 'Register New', command = regnew)
    detect_btn = tk.Button(tab1, text = 'Detect Face', command = detect)
    train_btn = tk.Button(tab1, text = 'Train Faces', command = trainSys)
    recognize_btn = tk.Button(tab1, text = 'Recognize Face', command = recFace)
    recognize_feed_btn = tk.Button(tab1, text = 'Recognize Feed', command = recFeed)
    remove_user_btn = tk.Button(tab1, text = 'Remove User', command = removeUser)
    exit_btn = tk.Button(tab1, text = 'Exit', command = exit_program)


    vba = PhotoImage(file='C:\\Users\\antre\\Desktop\\Year 3\\CS3IP16\\vision-based-attendance-analyser\\static\\logo.png')
    label_vba = Label(tab1, image = vba)


    # --- Grid --- #
    label_vba.pack()
    # label_vba.grid(row = 1, column = 10, padx = 15, pady = 35)
    # tab1_title.grid(row = 1, column = 1, padx = 15, pady = 15)
    # camtest_btn.grid(row = 2, column = 1, padx = 15, pady = 15)
    # register_btn.grid(row = 3, column = 1, padx = 15, pady = 15)
    # detect_btn.grid(row =4, column = 1, padx = 15, pady = 15)
    # train_btn.grid(row = 5, column = 1, padx = 15, pady = 15)
    # recognize_btn.grid(row = 6, column = 1, padx = 15, pady = 15)
    # recognize_feed_btn.grid(row = 7, column = 1, padx = 15, pady = 15)
    # remove_user_btn.grid(row = 8, column = 1, padx = 15, pady = 15)
    # exit_btn.grid(row = 9, column = 1, padx = 15, pady = 15)
    label_vba.pack()
    tab1_title.pack()
    camtest_btn.pack()
    register_btn.pack()
    detect_btn.pack()
    train_btn.pack()
    recognize_btn.pack()
    recognize_feed_btn.pack()
    remove_user_btn.pack()
    exit_btn.pack()


    # --- Tabs --- #
    tabs.pack(expand=1, fill='both') # adds the tabs into frame
    window.mainloop() # listens for actions 