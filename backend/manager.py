from flask import session, request, jsonify
from backend.dbconn import create_connection
from pymysql import MySQLError
from traceback import print_exc
from backend import alans_procedures


def get_site_name():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s25_get_site_for_manager(conn))
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def filter_manage_event():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s25_filter_event_get_attributes(conn))

    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def delete_event():
    conn = create_connection()
    try:
        alans_procedures._s25_delete_event(conn)
        return jsonify('success')
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def get_event_info():
    conn = create_connection()
    try:
        event = alans_procedures._s26_get_event_information(conn)
        event['staff'] = alans_procedures._s26_get_assigned_staff(conn)
        return jsonify(event), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def get_available_staff():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s27_get_available_staff(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def update_event():
    conn = create_connection()
    try:

        alans_procedures._s26_update_event_description(conn)
        data = request.get_json()
        
        with conn.cursor() as cursor:
            sql = 'call get_assigned_staff_for_event(%s, %s, %s)'
            args = [
                data.get('event_name'),
                session.get('site_name'),
                data.get('start_date')
            ]
            cursor.execute(sql, args)
            old_staffs = set(row['username'] for row in cursor.fetchall())
        staffs = set([el['username'] for el in data.get('staff')])


        to_add = [(staff, *args) for staff in staffs - old_staffs]
        to_delete = [(staff, *args) for staff in old_staffs - staffs]
        
        alans_procedures._s26_remove_assignments(conn, to_delete)
        alans_procedures._s26_add_assignments(conn, to_add)

        return ("success")
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()



def create_event():
    conn = create_connection()
    try:
        alans_procedures._s27_create_event(conn)
        return jsonify('success')
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def daily_event_info():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s26_get_daily_details(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def filter_staff():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s28_get_event_shifts(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def filter_site_report():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s29_filter_daily_details(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def daily_site_report():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s30_populate_table(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()

