CS4400 Team 70 Phase 3

Tasks: 
1. create HTMLs
2. A text file with all SQL statements for each task. (Follow the template in the Phase 2 design methodology).
A set or sequence of SQL statements may be required in order to complete a given task. However, in such cases, the last SQL statement should show the output according to the specification.
Views and nested queries may be used to support the tasks

Database
• MySQL v8.0 or later
• Must use InnoDB engine (ENGINE = InnoDB) [default on non-CoC servers - should be default on most local installations as well]

Back End: connects to the MySQL database in order to render the front end.
• NodeJS (Express)
• Python (Flask, PyMySQL)

Front End: renders the information passed from the back end.

Web Application
• HTML/CSS/JavaScript
• AngularJS (v1.x)
• Angular (v4.x)
• Vue.js
• React
• Bootstrap
• jQuery

Desktop Application
• Python
• PyQt4/PyQt5 with QtCore, QtGui, and QtWidgets • Electron • Qt (C++) using QtCore, QtGui, and QtWidgets.


### Backend
* `python3, flask, pymysql`

### DB
* Run `data/create_tables.sql` to create tables
* Run `data/insert_data.sql` to populate tables
* Run `data/procedures.sql` to create stored procedures used to run the backend (__REQUIRED TOO__)
* check `backend/dbconn.py to configure connection to db (db user and password)`

### Running backend
* When running flask: 
    * `export FLASK_APP=app.py` - point flask to starting script
    * `export FLASK_DEBUG=1`
    * __`flask run`__ 
