import pymysql
from flask import session, request, jsonify
from backend.dbconn import create_connection


def take_transit():
    if not session.get('logged_in'):
        return jsonify("not logged in"), 401
    conn = create_connection()
    data = request.get_json()
    try:
        with conn.cursor() as cursor:
            sql = f'call take_transit(%s, %s, %s, %s)'
            args = [session.get('username'),
                    data.get('type'),
                    data.get('route'),
                    data.get('date')]
            cursor.execute(sql, args)
        conn.commit()
    except pymysql.err.IntegrityError or KeyError as e:
        return jsonify(e.args[-1]), 400
    finally:
        conn.close()
    return jsonify("success"), 200


def filter_transits():
    if not session.get('logged_in'):
        return jsonify("not logged in"), 401
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = f'call take_transit_filter(%s, %s, %s, %s)'
            args = [request.args.get('type', None),
                    request.args.get('site', None),
                    request.args.get('low_price', None),
                    request.args.get('high_price', None)]
            cursor.execute(sql, args)
            result = cursor.fetchall()
            for row in result:
                row['price'] = float(row['price'])
            return jsonify(result), 200
    finally:
        conn.close()


def filter_transit_history():
    if not session.get('logged_in'):
        return jsonify("not logged in"), 401
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = f'call filter_transit_history(%s, %s, %s, %s, %s, %s)'
            args = [request.args.get('type', None),
                    request.args.get('site', None),
                    request.args.get('route', None),
                    request.args.get('start_date', None),
                    request.args.get('end_date', None),
                    request.args.get('username', None)]
            cursor.execute(sql, args)
            result = cursor.fetchall()
            for row in result:
                row['price'] = float(row['price'])
            return jsonify(result), 200
    finally:
        conn.close()


def get_all_sites():
    if not session.get('logged_in'):
        return jsonify("not logged in"), 401
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = "call get_site_names();"
            cursor.execute(sql)
            result = cursor.fetchall()
            return jsonify([row['site_name'] for row in result]), 200
    finally:
        conn.close()


def get_all_transport_types():
    if not session.get('logged_in'):
        return jsonify("not logged in"), 401
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = "select distinct type from transit;"
            cursor.execute(sql)
            result = cursor.fetchall()
            return jsonify([row['type'] for row in result]), 200
    finally:
        conn.close()
