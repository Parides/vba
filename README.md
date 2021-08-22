<div align="center">
  <img alt="logo" src="https://github.com/Parides/vba/blob/4c02d52aeb1fe2bcbae68f9dec399ea049015a99/web/css/dashboard.png" width="100"/>
  <h1>Vision Based Attendance Analyzer</h1>
  <p>Welcome to the first iteration of my final year project 👋</p>
</div>
<p align="center">
  <a href="www.google.com" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
</p>

## 📰 Description
VBA is an attendance monitoring system, that uses the OpenCV library for python, to identify individuals and log their attendance. Additionally, the project has a front end where an institution can manage their teachers, the teachers can manage their modules, students and their attendance, and the students can view their attendance analytics and manage their private data.

### ➡ [Video Demonstration of all functionalities](https://youtu.be/asec-YM0UjM)

## 🛠 Initialization & Setup 

#### Clone the repository

```sh
git clone https://github.com/Parides/vba.git
```
#### Install all dependencies

```sh
pip install -r requirements.txt
```
#### 

```sh
psql dbname < database_schema.sql
```
[More help here](https://www.postgresql.org/docs/9.1/backup-dump.html)

## 🚀 Building and Running

#### Initialize the attendance management system
```sh
python app.py
```
#### Initialize the attendance monitoring system
```sh
python api.py
```

## ⚠ How to start
1. Manually add a master account in the database (automatic functionality to be added in later versions)
2. Access the Flask Website and log in with the credentials created
3. Create new teachers accounts & modules with their associated teacher.
4. Create new student accounts
5. Assign students to modules using the teacher accounts

All other fucntionalities can be found in the [demo](https://youtu.be/asec-YM0UjM)
## Author

👤 **Andreas Paridis**

* Github: [@Parides](https://github.com/Parides)
* LinkedIn: [@parides](https://linkedin.com/in/parides)
