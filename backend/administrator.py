from flask import session, request, jsonify
from backend.dbconn import create_connection
from pymysql import MySQLError
from traceback import print_exc
from backend import alans_procedures




def filter_manage_user():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s18_get_information_for_tables(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def update_user_status():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s18_update_user_status(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def get_managers():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s19_populate_managers(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def filter_manage_site():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s19_get_manager_names_for_sites(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def get_unassigned_managers():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s20_get_unassigned_manager_names(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def get_site_info():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s20_get_site_info(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def update_site():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s20_edit_site(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def create_site():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s21_create_site(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def delete_site():
    conn = create_connection()
    try:
        alans_procedures._s19_delete_site(conn)
        return jsonify('success')
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()



def filter_manage_transit():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s22_get_info_for_table(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()



def transit_connected_sites():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s23_get_connected_sites(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()



def update_transit():
    conn = create_connection()
    try:
        data = request.get_json()

        alans_procedures._s23_update_transit_info(conn)


        with conn.cursor() as cursor:
            sql = f'call show_current_connected_sites(%s, %s)'
            args = [
                data.get('type'),
                data.get('route')
            ]
            cursor.execute(sql, args)
            old_sites = set(row.get('site_name') for row in cursor.fetchall())
        sites = set(data.get('sites'))

        to_add = [(data.get('type'), data.get('route'), site) for site in sites - old_sites]
        to_delete = [(data.get('type'), data.get('route'), site) for site in old_sites - sites]

        alans_procedures._s23_remove_connected_sites(conn, to_delete)
        alans_procedures._s23_add_connected_sites(conn, to_add)


        return jsonify("success")
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def create_transit():
    conn = create_connection()
    try:
        alans_procedures._s24_create_transit(conn)
        return jsonify("success")
    except MySQLError as e:
            print(e)
            return jsonify(str(e)), 400
    finally:
        conn.close()


def delete_transit():
    conn = create_connection()
    try:
        alans_procedures._s22_delete_transit(conn)
        return jsonify('success')
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()

