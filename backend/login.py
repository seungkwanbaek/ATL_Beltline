from flask import session, request, jsonify

from backend import alans_procedures
from backend.dbconn import create_connection


def login():
    conn = create_connection()

    try:
        with conn.cursor() as cursor:
            sql = "call user_login(%s, %s)"

            data = request.get_json()
            credentials = [data.get('email', ''), data.get('password', '')]
            cursor.execute(sql, credentials)
            result = cursor.fetchone()
            if result is None:
                return jsonify("no such username and password"), 400

            if result['status'] != 'Approved':
                return jsonify(f"Account is {result['status']}"), 400

            session['username'] = result['username']
            session['status'] = result['status']
            session['logged_in'] = True

            classification = _classify_user(cursor)

        if session.get('type') == 'manager':
            site_object = alans_procedures._s25_get_site_for_manager(conn)
            if site_object is None:
                session['site_name'] = None
            else:
                session['site_name'] = site_object.get('site_name')

        return jsonify({
            'username': session['username'],
            **classification}), 200
    finally:
        conn.close()


def _classify_user(cursor):
    classification = {'user_type': 'User'}
    sql = f"select * from employee where username = '{session['username']}'"
    cursor.execute(sql)
    result = cursor.fetchone()
    session['is_employee'] = result is not None
    if session['is_employee']:
        classification['user_type'] = 'Employee'

    sql = f"select * from visitor where username = '{session['username']}'"
    cursor.execute(sql)
    result = cursor.fetchone()
    session['is_visitor'] = result is not None
    if session['is_visitor']:
        classification['user_type'] = 'Visitor' if classification['user_type'] == 'User' else 'EmployeeVisitor'

    if session['is_employee']:
        tables = ['staff', 'manager', 'administrator']
        for table in tables:
            sql = f"select * from {table} where username = '{session['username']}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is not None:
                session['type'] = table
                classification['employee_type'] = table.capitalize()
                break

    return classification


def logout():
    session.clear()
    return jsonify("success")
