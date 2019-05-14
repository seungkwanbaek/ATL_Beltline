import pymysql
from flask import request, session, jsonify
from backend.dbconn import create_connection


def register():
    conn = create_connection()
    data = request.get_json()
    try:
        _add_user(conn, data.get('data'))
        _add_emails(conn, data=data.get('data'))

        if data.get('type') == 'Visitor' or data.get('type') == 'EmployeeVisitor':
            _add_visitor(conn, data.get('data'))

        if data.get('type') == 'Employee' or data.get('type') == 'EmployeeVisitor':
            _add_employee(conn, data.get('data'))
    except pymysql.err.IntegrityError or KeyError as e:
        return jsonify(e.args[-1]), 400

    finally:
        conn.close()

    return jsonify('success'), 200


def get_employee_profile():
    if not session.get('logged_in'):
        return jsonify("not logged in"), 401

    if not session.get('is_employee'):
        return jsonify(f"api not accessible for {session.get('is_employee')}"), 401
    conn = create_connection()

    try:
        with conn.cursor() as cursor:
            sql = f"call get_employee_profile('{session.get('username')}');"
            cursor.execute(sql)

            result = cursor.fetchone()
        emails = _get_emails(conn)
        result['emails'] = emails
        result['is_visitor'] = bool(session.get('is_visitor'))
        return jsonify(result), 200
    finally:
        conn.close()


def update_employee_profile():
    if not session.get('logged_in'):
        return jsonify("not logged in"), 401

    if not session.get('is_employee'):
        return jsonify(f"api not accessible for {session.get('is_employee')}"), 401
    conn = create_connection()

    try:
        with conn.cursor() as cursor:
            data = request.get_json()
            sql = 'call update_profile_employee(%s,%s,%s,%s)'
            args = [session.get('username'),
                    data.get('first_name'),
                    data.get('last_name'),
                    data.get('phone')]

            cursor.execute(sql, args)
        conn.commit()

        with conn.cursor() as cursor:
            old_sql = f"select email from user_email where username = '{session.get('username')}';"
            cursor.execute(old_sql)

            old_emails = set(row.get('email') for row in cursor.fetchall())
        emails = set(data.get('emails'))

        to_add = [(session.get('username'), email) for email in emails - old_emails]
        to_delete = [email for email in old_emails - emails]

        _add_emails(conn, emails=to_add)
        _delete_emails(conn, to_delete)
        if session['is_visitor'] != data.get('is_visitor'):
            session['is_visitor'] = data.get('is_visitor')
            _add_visitor(conn) if data.get('is_visitor') else _delete_visitor(conn)

    finally:
        conn.close()
    return jsonify('success'), 200


def _get_emails(conn):
    result = []
    with conn.cursor() as cursor:
        sql = f"select email from user_email where username = '{session.get('username')}'"
        cursor.execute(sql)
        result = cursor.fetchall()
    return [row['email'] for row in result]


def _add_user(conn, data):
    with conn.cursor() as cursor:
        sql_user = f'call add_user(%s, %s, %s, %s)'
        args = [data.get('username'),
                data.get('password'),
                data.get('first_name'),
                data.get('last_name')]
        cursor.execute(sql_user, args)
    conn.commit()



def _add_emails(conn, data=None, emails=None):
    if emails is None:
        emails = [(data.get('username'), email) for email in data.get('emails')]

    with conn.cursor() as cursor:
        sql = f'call add_email(%s, %s)'
        cursor.executemany(sql, emails)
    conn.commit()


def _delete_emails(conn, emails):
    with conn.cursor() as cursor:
        sql = 'call delete_email(%s)'
        cursor.executemany(sql, emails)
    conn.commit()


def _add_visitor(conn, data=None):
    if data is None:
        args = [session.get('username')]
    else:
        args = [data.get('username')]
    with conn.cursor() as cursor:
        sql = f'call add_visitor(%s)'
        cursor.execute(sql, args)
    conn.commit()


def _delete_visitor(conn):

    with conn.cursor() as cursor:
        sql = f'call delete_visitor(%s)'
        args = [session.get('username')]
        cursor.execute(sql, args)
    conn.commit()


def _add_employee(conn, data):
    with conn.cursor() as cursor:
        sql_user = f'call add_employee(%s, %s, %s, %s, %s, %s)'
        args = [data.get('username'),
                data.get('phone'),
                data.get('address'),
                data.get('city'),
                data.get('state'),
                data.get('zipcode')]
        cursor.execute(sql_user, args)
    conn.commit()

    user_type = data.get('user_type')
    if user_type == 'Manager':
        _add_manager(conn, data)
    elif user_type == 'Staff':
        _add_staff(conn, data)


def _add_manager(conn, data):
    with conn.cursor() as cursor:

        sql = f'call add_manager(%s)'
        args = [data.get('username')]
        cursor.execute(sql, args)
    conn.commit()


def _add_staff(conn, data):
    with conn.cursor() as cursor:

        sql = f'call add_staff(%s)'
        args = [data.get('username')]
        cursor.execute(sql, args)
    conn.commit()
