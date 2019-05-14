Database
• MySQL v8.0 or later
• Must use InnoDB engine (ENGINE = InnoDB) [default on non-CoC servers - should be default on most local installations as well]

Back End: connects to the MySQL database in order to render the front end.
• Python (Flask)

Web Application
• AngularJS (v1.x)

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
