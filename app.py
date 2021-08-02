import eel
import test, camtest, newface, recognize, train, removeuser,updateapp,menu
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import test, camtest, newface, recognize, train, removeuser,updateapp
from tkinter import simpledialog
from ttkthemes import themed_tk
import tkinter.messagebox
import connections

query = f"SELECT module_id FROM modules"
result = connections.fetch_data(connections.connect_to_db(), query)
modules = []
for module_id in result:
    modules.append(module_id[0])
# Set web files folder
eel.init('web')

@eel.expose # exposes the function to the HTML PAGE
def testcam():
    return camtest.camtest() # returns the external python function that handles the face detection

@eel.expose # exposes the function to the HTML PAGE
def detect():
    return test.facedetect() # returns the python function that handles the face detection

@eel.expose
def recognizeFace(session_info):
    if session_info['module_code'] in modules:
        return recognize.recognize(session_info)
    else:
        return False

@eel.expose # exposes the function to the HTML PAGE
def recognizeFeed(session_info):
    if session_info['module_code'] in modules: # checks if module code is valid
        return recognize.recognize_feed(session_info) # returns the python function that handles the face detection
    else:
        return False
        
@eel.expose
def exit_program():
    return exit()

eel.start('hello.html', size=(1280, 1080))  # Start
