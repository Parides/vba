from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash, send_from_directory
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import datetime
import time as tim
import hashlib
import os
from werkzeug.utils import secure_filename
import connections
import json

#from flask_cors import CORS, cross_origin

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(FILE_PATH, 'prerecorded\\')
DOWNLOAD_FOLDER = os.path.join(FILE_PATH, 'data_requests')
ALLOWED_EXTENSIONS = {'mp4'}

# * ---------- Create App --------- *
# Init the app
app = Flask(__name__)
app.secret_key = "secretkey"
app.permanent_session_lifetime = timedelta(days = 365)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # no cache


# To avoid cors erros
#CORS(app, support_credentials=True)


@app.route("/")
def home():
    # return render_template("index.html")
    return redirect(url_for("user"))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('profile'))

@app.route("/login", methods = ["POST", "GET"])
def login():

    if request.method == "POST":
        user_id = request.form["username"]
        user_password = (hashlib.md5(request.form["password"].encode())).hexdigest()

        query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
        result = connections.fetch_data(connections.connect_to_db(), query)

        if result:
            if user_password == result[0][3]:
                if 'permanent' in request.form:
                    session.permanent = True

                else:
                    session.permanent = False

                flash(f"Login Successful!. Welcome back {result[0][2]}", category= "success")
                session["user_id"] = user_id
                session["user_name"] = result[0][2]
                session["user_permission"] = result[0][1]
            
                if session["user_permission"] == 1:
                    return redirect(url_for("master"))
                elif session["user_permission"] == 2:
                    return redirect(url_for("admin"))
                elif session["user_permission"] == 3:
                    return redirect(url_for("user"))
            else:
                flash("Wrong Credentials!", category='danger')
                return redirect(url_for("login"))
        else:
            flash("Wrong Credentials!", category='danger')
            return redirect(url_for("login"))
    else:
        if "user_id" in session:
            return redirect(url_for('profile'))
        else:
            return render_template("login.html")

@app.route("/admin", methods = ["POST", "GET"])
def admin():
    if "user_id" in session:
        if session["user_permission"] == 2:
            if request.method == "POST":
                
                users_in_module_new = request.form.getlist('select1')
                users_not_in_module_new = request.form.getlist('select2')

                module_responsible = get_responsible(session['user_id'])
                module_users = get_module_users(module_responsible)

                existing_module_users = []
                for row in module_users:
                    existing_module_users.append(row[0])

                for row in users_in_module_new:
                    if row not in existing_module_users:
                        add_user_to_module(module_responsible, row)
                        print("Adding " + row + " in the module")

                for row in users_not_in_module_new:
                    if row in existing_module_users:
                        print("Removing " + row + " from module")
                        remove_user_from_module(module_responsible, row)

            else:
                module_responsible = get_responsible(session['user_id'])
                all_users = get_all_users(module_responsible)
                module_users = get_module_users(module_responsible)
                if module_users:
                    attendance_labels, attendance_values, average_session_attendance = attendance_per_session(module_responsible, len(module_users))
                    user_attendance = get_attendance_admin(module_responsible)
                else:
                    attendance_labels, attendance_values, average_session_attendance = [], [], []
                    user_attendance = []
                
                all_sessions = get_all_sessions(module_responsible)
                if all_sessions:
                    all_absenses = get_absenses(module_responsible, module_users, all_sessions)
                else:
                    all_absenses = []
                return render_template("admin.html", user_name = session["user_name"], user_id = session['user_id'], user_attendance = user_attendance, module_users = module_users, all_users = all_users, absences = all_absenses, sessions = all_sessions, attendance_labels = attendance_labels, attendance_values = attendance_values, average_attendance = average_session_attendance)              

            return redirect(url_for("profile"))
        
        else:
            return redirect(url_for("profile"))

    else:
        return redirect(url_for("profile"))

def get_responsible(admin_id):
    get_responsible_module_query = f"SELECT module_id FROM admin WHERE user_id = '{admin_id}'"
    get_responsible_module = connections.fetch_data(connection = connections.connect_to_db(), query = get_responsible_module_query)

    if get_responsible_module:
        get_responsible_module = get_responsible_module[0][0]
        return get_responsible_module
    else:
        return flash("No responsibility yet. Please contact IT department", category='danger')
   
def get_module_users(module_id):
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        cursor = connection.cursor()

        module_users = f"SELECT users_modules.user_id, user_name FROM users_modules RIGHT JOIN users ON users_modules.user_id = users.user_id WHERE users_modules.module_id = '{module_id}'"
        # NEED TO ADD ANOTHER JOIN FOR ATTENDANCES
        cursor.execute(module_users)
        result = cursor.fetchall()


        if result:
            return result

        else:
            module_users = []
            flash("No users under this module yet. If this is wrong contact the IT department", category='danger')
            return module_users


    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
        flash("Something went wrong please try again later", category='danger')

    
    finally:
        connection.commit()

        if connection:
            cursor.close()
            connection.close()
            print("CONNECTION CLOSED")

def get_attendance_admin(module_id):
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        cursor = connection.cursor()

        module_users = f"SELECT session_id, attendance.user_id, attendance_time FROM attendance RIGHT JOIN admin ON attendance.module_id = admin.module_id  WHERE attendance.module_id = '{module_id}'"
        # NEED TO ADD ANOTHER JOIN FOR ATTENDANCES
        cursor.execute(module_users)
        result = cursor.fetchall()


        if result:
            user_attendance = []

            
            for row in result:
                session_id = row[0]
                user_id = row[1]
                # user_id = row[2]
                attendance_time = row[2].strftime("%Y-%m-%d %H:%M:%S")
                # attendance_capture = row[4]

                # if user
                row_attendance = [session_id, user_id, attendance_time]
                #if admin
                #TODO

                user_attendance.append(row_attendance)

        else:
            return flash("No responsibility yet. Please contact IT department", category='danger')


    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
        flash("Something went wrong please try again later", category='danger')

    
    finally:
        connection.commit()

        if connection:
            cursor.close()
            connection.close()
            print("CONNECTION CLOSED")
    
    return user_attendance

def get_all_users(module_code):
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        cursor = connection.cursor()

        module_users = f"SELECT DISTINCT ON (users.user_id) users.user_id, users.user_name FROM users WHERE users.permissions_id = '3' AND users.user_id NOT IN (SELECT users_modules.user_id FROM users_modules WHERE  users_modules.module_id = '{module_code}')"
        cursor.execute(module_users)
        result = cursor.fetchall()

        if result:
            all_users = []

            
            for row in result:
                user_id = row[0]
                user_name = row[1]

                current_user = [user_id, user_name]

                all_users.append(current_user)

        else:
            all_users = []
            return all_users
            flash("No responsibility yet. Please contact IT department", category='danger')


    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
        flash("Something went wrong please try again later", category='danger')

    
    finally:
        connection.commit()

        if connection:
            cursor.close()
            connection.close()
            print("CONNECTION CLOSED")
    
    return all_users    

def remove_user_from_module(module_id, user_id):
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        cursor = connection.cursor()
        
        delete_user = f"DELETE FROM public.users_modules WHERE user_id = '{user_id}' and module_id = '{module_id}'"

        cursor.execute(delete_user)

    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)


    finally:
        connection.commit()

        if connection:
            cursor.close()
            connection.close()
            print("CONNECTION CLOSED")

def add_user_to_module(module_id, user_id):
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        cursor = connection.cursor()
        
        add_user_to_module = f"INSERT INTO public.users_modules( module_id, user_id, attendance_flag) VALUES ('{module_id}', '{user_id}', 'false');"

        cursor.execute(add_user_to_module)

    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)


    finally:
        connection.commit()

        if connection:
            cursor.close()
            connection.close()
            print("CONNECTION CLOSED")

def get_absenses(module_id, module_users, all_sessions):
    
    absences = []
    for user_id in module_users:
        query = f"SELECT module_sessions.session_id, attendance.user_id, module_sessions.session_name FROM module_sessions JOIN attendance ON module_sessions.module_id = attendance.module_id WHERE module_sessions.session_id NOT IN ( SELECT DISTINCT ON (attendance.session_id) attendance.session_id FROM attendance WHERE attendance.user_id = '{user_id[0]}' ) AND module_sessions.module_id = '{module_id}' AND attendance.user_id = '{user_id[0]}' GROUP BY module_sessions.session_id, attendance.user_id"
    
        result = connections.fetch_data(connection=connections.connect_to_db(),query=query)

        if result != 0:
            for row in result:
                absences.append(row)
        else:
            for session in all_sessions:
                new = [session[0], user_id[0], session[1]]
                absences.append(new)
                
    return absences
    
def get_all_sessions(module_id):
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        cursor = connection.cursor()
        
        add_user_to_module = f"SELECT module_sessions.session_id, module_sessions.session_name, module_sessions.session_date FROM module_sessions WHERE module_sessions.module_id = '{module_id}'"

        cursor.execute(add_user_to_module)

        result = cursor.fetchall()

        if result:
            return result

        else:
            result = []
            return result

    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)


    finally:
        connection.commit()

        if connection:
            cursor.close()
            connection.close()
            print("CONNECTION CLOSED")

def attendance_per_session(module_id, eligible_users):

    labels = []
    datasets = []
    average_session_attendance = []

    #get all sessions
    get_all_sessions_query = f"SELECT session_id FROM module_sessions WHERE module_id = '{module_id}'"
    get_all_sessions = connections.fetch_data(connection = connections.connect_to_db(), query = get_all_sessions_query)

    #get all attendances for that session
    if get_all_sessions:
        for session_id in get_all_sessions:
            session_id = session_id[0]
            get_session_attendance_query = f"SELECT count (session_id) FROM attendance WHERE module_id = '{module_id}' AND session_id = '{session_id}'"
            get_session_attendance = connections.fetch_data(connection = connections.connect_to_db(), query = get_session_attendance_query)[0][0]

            labels.append(session_id)

            session_attendance_percentage = round(get_session_attendance / eligible_users,2)
            datasets.append(session_attendance_percentage)

            average_session_attendance.append(session_attendance_percentage)

        average_session_attendance = round(sum(average_session_attendance) / len(average_session_attendance),2)
    
    return labels, datasets, average_session_attendance
   
@app.route("/profile", methods = ["POST", "GET"])
def profile():
    if "user_id" in session:
        if session["user_permission"] == 1:
            return redirect(url_for("master"))  
        elif session["user_permission"] == 2:
            return redirect(url_for("admin"))  
        elif session["user_permission"] == 3:
            return redirect(url_for("user"))     
    else:
        flash("To view your profile please log in", "danger")
        return render_template("login.html") 

@app.route("/user", methods = ["POST", "GET"])
def user():

    if "user_id" in session:
        if session["user_permission"] == 3:
            user_id = session["user_id"]
            user_name = session["user_name"]
            if request.method == "POST":
                user_password = (hashlib.md5(request.form["user_password"].encode())).hexdigest()
                change_password(user_id, user_password)


            modules = get_modules(user_id)
            if modules:
                attendance_per_module = get_threshhold(modules, user_id)
                attendance = get_attendance(user_id)
                per_module_attendance_labels, per_module_attendance_values = get_attendance_percentage(user_id, modules)
                absences = get_absenses_user(user_id, modules)
            else:
                modules = []
                attendance = []
                attendance_per_module = []
                per_module_attendance_labels, per_module_attendance_values = [],[]
            # return render_template("user.html", user_id = user_id, attendance = attendance, user_name = user_name)

            return render_template("user.html", user_id = user_id, absences = absences, attendance = attendance, user_name = user_name, attendance_per_module = attendance_per_module, chart_labels = per_module_attendance_labels, chart_data = per_module_attendance_values)

        else:
            return redirect(url_for("login"))
    else:
        flash("Please login first", category='danger')
        return redirect(url_for("login"))

def get_attendance(user_id):

    user_attendance = []

    get_uset_attendance_query = f"SELECT attendance.module_id, module_sessions.session_name, attendance.attendance_time FROM attendance RIGHT JOIN module_sessions ON attendance.session_id = module_sessions.session_id WHERE attendance.user_id = '{user_id}'"
    get_uset_attendance = connections.fetch_data(connection = connections.connect_to_db(), query = get_uset_attendance_query)
 
    if get_uset_attendance:
        for row in get_uset_attendance:
            row_attendance = []
            module_id = row[0]
            session_name = row[1]
            attendance_time = row[2].strftime("%Y-%m-%d %H:%M:%S")

            row_attendance = [module_id, session_name, attendance_time]
            user_attendance.append(row_attendance)     

    return user_attendance

def get_absenses_user(user_id, modules):
        
    absences = []
    for module_id in modules:

        query = f"SELECT module_sessions.session_id, attendance.module_id, module_sessions.session_date FROM module_sessions JOIN attendance ON module_sessions.module_id = attendance.module_id WHERE module_sessions.session_id NOT IN ( SELECT DISTINCT ON (attendance.session_id) attendance.session_id FROM attendance WHERE attendance.user_id = '{user_id}' ) AND module_sessions.module_id = '{module_id}' AND attendance.user_id = '{user_id}' GROUP BY module_sessions.session_id, attendance.user_id, attendance.module_id"
        result = connections.fetch_data(connection=connections.connect_to_db(),query=query)

        if result != 0:
            for row in result:
                absences.append(row)
        else:
            all_sessions = get_all_sessions(module_id)
            for session in all_sessions:
                new = [session[0], module_id, session[2]]
                absences.append(new) 

    return absences
    

def change_password(user_id, user_password):

    
    committed = 1

    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        cursor = connection.cursor()
        
        change_password = f"UPDATE users SET user_password = '{user_password}' WHERE user_id='{user_id}'"
        cursor.execute(change_password)

    except (Exception, psycopg2.DatabaseError) as error:
        committed = 0
        flash("Something went wrong")
        print("ERROR DB: ", error)


    finally:
        connection.commit()

        if committed == 1:
            flash("Password Changes successfully", category = "success")

        if connection:
            cursor.close()
            connection.close()
            print("CONNECTION CLOSED")

def get_modules(user_id):
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        cursor = connection.cursor()
        
        get_threshold = f"SELECT module_id FROM users_modules WHERE user_id = '{user_id}'"

        cursor.execute(get_threshold)
        result = cursor.fetchall()

        if result:
            modules = []

            for row in result:
                modules.append(row[0])
                
            return modules
    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)


    finally:
        connection.commit()

        if connection:
            cursor.close()
            connection.close()
            print("CONNECTION CLOSED")

def get_threshhold(module_ids, user_id):
    
    attendance_per_module = []

    for module_id in module_ids:
        get_module_threshold_query = f"SELECT module_threshhold FROM modules WHERE module_id = '{module_id}'"
        get_module_threshold = connections.fetch_data(connection = connections.connect_to_db(), query = get_module_threshold_query)[0][0]

        get_total_sessions_query = f"SELECT COUNT(module_id) FROM module_sessions WHERE module_id = '{module_id}'"
        get_total_sessions = connections.fetch_data(connection = connections.connect_to_db(), query = get_total_sessions_query)[0][0]

        get_sessions_attended_query = f"SELECT COUNT({user_id}) AS sessions_attended FROM attendance WHERE module_id = '{module_id}' AND user_id = '{user_id}'"
        get_sessions_attended = connections.fetch_data(connection = connections.connect_to_db(), query = get_sessions_attended_query)[0][0]
        
        absences_remaining = get_module_threshold - (get_total_sessions - get_sessions_attended)

        attendance = [module_id, get_total_sessions, get_sessions_attended, get_module_threshold, absences_remaining]
        attendance_per_module.append(attendance)
        
    return attendance_per_module
    

def get_attendance_percentage(user_id, modules):
    
    labels = []
    values = []

    for module_id in modules:
        labels.append(module_id)

        count_attendance_query = f"SELECT COUNT(attendance.user_id) FROM attendance WHERE module_id = '{module_id}' and attendance.user_id = '{user_id}' GROUP BY module_id"
        count_attendance = connections.fetch_data(connection = connections.connect_to_db(), query = count_attendance_query)

        count_module_sessions_query = f"SELECT COUNT(module_sessions.session_id) FROM module_sessions WHERE module_sessions.module_id = '{module_id}'"
        count_module_sessions = connections.fetch_data(connection = connections.connect_to_db(), query = count_module_sessions_query)

        if count_attendance:
            attendance_percentage = round(count_attendance[0][0] / count_module_sessions[0][0], 2)
            values.append(attendance_percentage)

    return labels, values
@app.route("/upload", methods = ["POST", "GET"])
def upload_file():
    # file = request.files["upload_file"]

    # try:
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    # except Exception as error:
    #     print(error)


    if request.method == 'POST':
        # check if the post request has the file part
        if 'upload_file' not in request.files:
            flash('File Not Uploaded! No file found', category='danger')
            return redirect(request.url)
        file = request.files['upload_file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash("Upload Unsucessful. No file found", category= 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # unme = session["user_name"].strip()
            time_capture = tim.time() # capture current time
            date_uploaded = datetime.datetime.fromtimestamp(time_capture).strftime('%Y_%m_%d') # date in YYYY-MM-DD HH:MM:SS format

            filename = session["user_id"] + "_" + session["user_name"].replace(" ","") + "_" +date_uploaded + ".mp4"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("File succesfully uploaded!", category = 'success')
            user_biometric_consent = request.form["user_biometric_consent"]
            user_name = session['user_id']
            update_user_consent(user_biometric_consent, user_name)
            # return redirect(url_for('uploaded_file',filename=filename))
        else:
            flash("Upload Unsucessful. Only '.mp4' files are allowed", category= 'danger')
    return redirect(url_for("profile"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def update_user_consent(consent, user_id):
    committed = 1
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        cursor = connection.cursor()
        
        if consent == 'on':
            update_consent = f"UPDATE users SET user_biometric_consent= '{consent}' WHERE user_id = '{user_id}'"
            cursor.execute(update_consent)

        elif consent == 'off':
            update_consent = f"UPDATE users SET user_biometric_consent= '{consent}' WHERE user_id = '{user_id}'"
            cursor.execute(update_consent)

    except (Exception, psycopg2.DatabaseError) as error:
        committed = 0
        print("ERROR DB: ", error)
        flash("Something went wrong please try again later", category= 'danger')

    
    finally:
        connection.commit()
        
        if committed == 1:
            flash("Biometric Consent Updated Successfully", category='success')

        if connection:
            cursor.close()
            connection.close()
            print("CONNECTION CLOSED")

    
    return redirect(url_for("profile"))

def update_attendance_flag(user_id, module_id):
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vj017877_vba")

        cursor = connection.cursor()
        
        update_flag = f"UPDATE public.users_modules SET attendance_flag= 'True' WHERE user_id = '{user_id}' and module_id = '{module_id}';"
        cursor.execute(update_flag)
                
    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)


    finally:
        connection.commit()

        if connection:
            cursor.close()
            connection.close()
            print("CONNECTION CLOSED")

@app.route("/logout")
def logout():
    if "user_id" in session:
        user = session["user_name"]
        flash(f"You have been logged out!", "danger")
        session.pop("user_id", None)
        session.pop("user_name", None)
        session.pop("user_permission", None)
        session.pop("email", None)
    else:
        flash("You are not logged in!")
    return redirect(url_for("login"))

@app.route("/register",  methods = ["POST", "GET"])

def register():
    if "user_id" in session:
        flash("Please logout first", "info")
        return redirect(url_for("user"))

    if request.method == "POST":
        succ = 0
        session.permanent = True
        user_fullname = request.form["name"]
        user_name = request.form["username"]
        password = (hashlib.md5(request.form["password"].encode())).hexdigest()
        time_capture = tim.time() # capture current time
        user_register = datetime.datetime.fromtimestamp(time_capture).strftime('%Y-%m-%d %H:%M:%S') # date in YYYY-MM-DD HH:MM:SS format

        #h = hashlib.md5(password.encode())
        #print(h.hexdigest())
        
        try:
            connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vba")

            cursor = connection.cursor()
            find_username = f"SELECT * FROM webusers WHERE webusers_username = '{user_name}'"
            cursor.execute(find_username)
            result = cursor.fetchall()

            if result:
                flash("Username Already Exists", category= 'danger')
                return redirect(url_for("register")) 
            else:
                succ = 1
                all_data = f"INSERT INTO webusers(webusers_username, webusers_password, webusers_fullname, webusers_datetime_registered) VALUES ('{user_name}', '{password}', '{user_fullname}', '{user_register}')"
                cursor.execute(all_data)


        except (Exception, psycopg2.DatabaseError) as error:
            print("ERROR DB: ", error)

        
        finally:
            connection.commit()

            if connection:
                cursor.close()
                connection.close()
                print("CONNECTION CLOSED")
            
            if succ:
                flash("Login Successful!")

        return redirect(url_for("user"))
    else:
        if "user_id" in session:
            flash("Already Logged in!")
            return redirect(url_for("user"))
    
    return render_template("register.html")

@app.route("/master", methods = ["POST", "GET"])
def master():
    
    if "user_id" in session:
        if session["user_permission"] == 1:
            if request.method == "POST":
                
                
                session.permanent = True
                
                

            else:
                return render_template("master.html", user_name = session["user_name"], user_id = session['user_id'])

            return render_template("master.html", user_name = session["user_name"])
        
        else:
            return redirect(url_for("profile"))

        return render_template("master.html", user_name = session["user_name"], user_id = session['user_id'])


    else:
        return redirect(url_for("profile"))

def create_user(data):
          
    user_id = data["user_id"]
    user_name = data["user_name"]
    user_password = data["user_password"]
    user_permission = data["user_permission"]
    user_video_location = data["user_video_location"]
    time_capture = tim.time() # capture current time
    user_timestamp_registered = datetime.datetime.fromtimestamp(time_capture).strftime('%Y-%m-%d %H:%M:%S')
    user_biometric_consent = False

    existing_username = f"SELECT * FROM users where user_id = '{user_id}'"
    result = connections.fetch_data(connections.connect_to_db(), existing_username)

    if result:
        flash("Username Already Exists", category='danger')

    else:
        insert_new_user = f"INSERT INTO public.users(user_id, permissions_id, user_name, user_password, user_video_location, user_timestamp_registered, user_biometric_consent) VALUES ('{user_id}', '{user_permission}', '{user_name}', '{user_password}', '{user_video_location}','{user_timestamp_registered}', '{user_biometric_consent}');"

        result = connections.insert_or_delete(connections.connect_to_db(), insert_new_user)

        if result == 1:
            flash("New user created successfully", category='success')
        else:
            flash("Something went terribly wrong", category='danger')
    
    return redirect(url_for('master'))

def create_module(data):

    committed = 1

       
    module_id = data["module_id"]
    module_name = data["module_name"]
    module_threshold = data["module_threshold"]
    time_capture = tim.time() # capture current time
    module_timestamp_registered = datetime.datetime.fromtimestamp(time_capture).strftime('%Y-%m-%d %H:%M:%S')



    existing_module = f"SELECT * FROM modules where module_id = '{module_id}'"
    result = connections.fetch_data(connections.connect_to_db(), existing_module)

    if result:

        committed = 0
        flash("Error: Module ID Already Exists", category= 'danger')     

    else:
        
        insert_new_module = f"INSERT INTO modules(module_id, module_name, module_threshhold, module_timestamp_registered) VALUES ('{module_id}', '{module_name}', '{module_threshold}', '{module_timestamp_registered}');"
        result = connections.insert_or_delete(connections.connect_to_db(), insert_new_module)

    if result == 1:
        flash("New user created successfully", category='success')
    else:
        flash("Something went terribly wrong", category='danger')
###############################--------------------##########################

# * ------------------------ API ----------------------- *

@app.route("/manualattendance", methods = ['POST'])
def manualattendance():
    to_be_added_attendnace = request.form.getlist('inModule')
    session_of_attendance = request.form.getlist('sessionNames')
    module_responsible = get_responsible(session['user_id'])
    time_capture = tim.time() # capture current time
    manual_capture_time = datetime.datetime.fromtimestamp(time_capture).strftime('%Y-%m-%d %H:%M:%S')


    for session_id in session_of_attendance:
        query = "INSERT INTO public.attendance( module_id, session_id, user_id, attendance_time, attendance_capture) VALUES "
        for user_id in to_be_added_attendnace:
            query += f"('{module_responsible}', '{session_id}', '{user_id}', '{manual_capture_time}' , 'MANUAL'),"

        
    query = query[:-1]

    result = connections.insert_or_delete(connections.connect_to_db(), query)

    if result == 1:
        flash("Attendance added successfully", category='success')
    else:
        flash("Something went wrong! Plase make sure you are not trying to add an existing attendanace", category='danger')
    print(1)

    return redirect(url_for('profile'))

@app.route("/changepass", methods = ['POST'])
def changepass():
    
    if 'user_id' in session:
        user_id = session['user_id']
        new_password = (hashlib.md5(request.form["user_password"].encode())).hexdigest()
        
        query = f"UPDATE users SET user_password = '{new_password}' WHERE user_id='{user_id}'"
        result = connections.insert_or_delete(connections.connect_to_db(),query)

        if result:
            flash("Password Changed Successfully", category='success')
        else:
            flash("Something went wrong", category='danger')

        return redirect(url_for("profile"))

    else:
        flash("Something went wrong", category='danger')
        return redirect(url_for("profile"))

@app.route("/removebio", methods = ['POST'])
def removebio():
    if 'user_id' in session:
        user_id = session['user_id']
        feedback = request.form["user_feedback"]
        
        
        query = f"UPDATE users SET user_biometric_consent= 'off' WHERE user_id = '{user_id}'"
        result = connections.insert_or_delete(connections.connect_to_db(),query)

        if result == 1:
            flash("Your request has been processed", category='success')
        else:
            flash("Something went wrong", category='danger')

        return redirect(url_for("profile"))

    else:
        flash("Something went wrong", category='danger')
        return redirect(url_for("profile"))


@app.route("/adduser", methods = ['POST'])
def adduser():
    
    module_or_user = request.form["module_or_user"]
    data = {}
    
    user_id = request.form["username"]
    user_name = request.form["name"]
    user_password = (hashlib.md5(request.form["password"].encode())).hexdigest()
    user_permission = request.form["permission"]

    data["user_id"] = user_id
    data["user_name"] = user_name
    data["user_password"] = user_password
    data["user_permission"] = user_permission
    data["user_video_location"] = None


    create_user(data)

    return redirect(url_for('profile'))


@app.route("/addmodule", methods = ['POST'])
def addmodule():

    module_or_user = request.form["module_or_user"]
    data = {}

    module_id = request.form["module_id"]
    module_name = request.form["module_name"]
    module_threshold = request.form["module_threshold"]

    data["module_id"] = module_id
    data["module_name"] = module_name
    data["module_threshold"] = module_threshold

    create_module(data)

    return redirect(url_for('master'))
    
@app.route("/api/get_attendance", methods = ["GET"])
def get_attendance_user():
    try:
        connection = psycopg2.connect(user = "postgres", password = "domenico13qaz", host = "127.0.0.1", database = "vba")

        cursor = connection.cursor()
        
        username = 27017877
        all_data = f"SELECT * FROM attendance"

        cursor.execute(all_data)
        result = cursor.fetchall()
        connection.commit()

        if result:
            data = []

            for row in result:
                json = {}
                json['user_id'] = row[0]
                json['date'] = row[2].strftime("%Y-%m-%d")
                json['time'] = row[3].strftime("%H:%M:%S")
                # session_id = row[0]
                # date = row[2].strftime("%Y-%m-%d %H:%M:%S")
                # time = row[3].strftime("%H:%M:%S")
                # atndc = [session_id, date, time]

                data.append(json)        

        else:

            print("something went wrong")


    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)


    finally:
        connection.commit()

        if connection:
            cursor.close()
            connection.close()
            print("CONNECTION CLOSED")

    return jsonify(data)
    #return render_template("jquerytest.html", data = json_to_send)

@app.route("/api/get_all_attendance")
def get_all_attendance():
    get_all_attendance = f"SELECT * FROM attendance"
    get_all_attendance = connections.fetch_data(connection = connections.connect_to_db(), query = get_all_attendance)

    return jsonify(get_all_attendance)

@app.route("/download_data", methods = ["POST"])
def download_data():
    if "user_id" in session:
        user_id = session['user_id']

        attendance = get_attendance(user_id)
        # attendance = jsonify(attendance)
        attendance = json.dumps(attendance)
    
    file_path = DOWNLOAD_FOLDER
    file_name = user_id + "_data_requested.txt"
    attendnace_data = open(os.path.join(DOWNLOAD_FOLDER,file_name), "w")
    attendnace_data.write(attendance)
    attendnace_data.close()

    try:
        return send_from_directory(file_path, file_name, as_attachment = True)
    except Exception:
        flash("Something went wrong. Please try again later", category='danger')
        return redirect(url_for("profile"))

@app.route("/test")
def test():
    return render_template("master(old).html")
# * -------------------- Run Server -------------------- *

if __name__ == '__main__':
    # * --- DEBUG MODE: --- *
    # app.run(host='127.0.0.1', port=5000, debug=True)
    # app.run(host='127.0.0.1', port=5000)
    # app.run(host = '192.168.0.10')
    app.run(host='192.168.0.10', port=5000, debug=True, ssl_context='adhoc')