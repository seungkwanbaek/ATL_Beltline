from flask import session, request, jsonify
from backend.dbconn import create_connection
from pymysql import MySQLError
from traceback import print_exc
from backend import alans_procedures, bryans_procedures



def filter_explore_event():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s33_filter_events(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def event_detail():
    conn = create_connection()
    try:
        return jsonify(bryans_procedures._s34_visitor_view_event(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def log_event_visit():
    conn = create_connection()
    try:
        bryans_procedures._s34_log_visit_event(conn)
        return jsonify("success"), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def filter_explore_site():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s35_filter_sites(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()



def get_transit_details():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s36_populate_table_with_filter(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def log_transit_visit():
    conn = create_connection()
    try:
        bryans_procedures._s36_log_transit(conn)
        return jsonify("success"), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()



def get_site_details():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s37_get_site_detail(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def log_site_visit():
    conn = create_connection()
    try:
        bryans_procedures._s37_log_visit_site(conn)
        return jsonify("success"), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def visit_history():

    conn = create_connection()
    try:
        return jsonify(bryans_procedures._s38_filter_visits(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


