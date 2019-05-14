from flask import session, request, jsonify
from backend.dbconn import create_connection
from pymysql import MySQLError
from traceback import print_exc
from backend import alans_procedures



def filter_schedule():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s31_get_staff_counts(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()


def schedule_details():
    conn = create_connection()
    try:
        return jsonify(alans_procedures._s32_view_staff_detail(conn)), 200
    except MySQLError as e:
        print(e)
        return jsonify(str(e)), 400
    finally:
        conn.close()