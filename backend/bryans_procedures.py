import pymysql
from flask import session, request, jsonify
from backend.dbconn import create_connection


"""
Return event_name, site_name, start_date, end_date, price, ticket_remaining, 
description
"""
def _s34_visitor_view_event(conn):
    with conn.cursor() as cursor:
        sql = f'call visitor_view_event(%s, %s, %s)'
        args = [
            request.args.get('event_name', None),
            request.args.get('site_name', None),
            request.args.get('start_date', None),
        ]
        cursor.execute(sql, args)
        result = cursor.fetchone()
        result['price'] = float(result['price'])
        return result

"""
post username, event_name, site_name, start_date, date

Return None
"""
def _s34_log_visit_event(conn):
    with conn.cursor() as cursor:
        sql = f'call log_visit_event(%s, %s, %s, %s, %s)'
        data = request.get_json()
        args = [
                session.get('username'),
                data.get('event_name', None),
                data.get('site_name', None),
                data.get('start_date', None),
                data.get('date', None)
            ]
        cursor.execute(sql, args)
    conn.commit()

"""
Return site_name, event_count, total_visits, my_visits
"""
def _s35_(conn):
    with conn.cursor() as cursor:
        sql = f'call get_transit_information(%s, %s)'
        args = [
            request.args.get('site_name', None),
            request.args.get('type', None)
        ]
        cursor.execute(sql, args)
        result = cursor.fetchall()
        return result

# create procedure filter_explore_sites(in in_site_name varchar(30), \
#                                                in_manager_username varchar(15),
#                                                 in in_start_date Date,
#                                                 in in_end_date Date,
#                                                 in_open_everyday bit)
# begin
# select name, event_count, total_visits, my_visits from site
# JOIN visit_site ON name = site_name
# where (in_site_name is NULL OR in_site_name = name)
# and (in_open_everyday is NULL OR in_open_everyday = open_everyday)
# and (in_start_date is null or in_end_date is null or date between in_start_date and in_end_date)
# and (in_manager_username is NULL OR manager_username = in_manager_username);
# end //
#
#
# select connect.type, connect.route, price, count(*) as connected_sites from connect
# JOIN transit ON connect.type = transit.type and connect.route = transit.route
# where (connect.type, connect.route) in (select type, route from transit where (in_type is null or type = in_type) and (type, route) in (select type, route from connect where site_name = in_site))
# group by transit.type, transit.route;

"""
Return transit_type, transit_route, price, number of connected sites
"""
def _s36_view_site(conn):
    with conn.cursor() as cursor:
        sql = f'call get_transit_information(%s, %s)'
        args = [
            request.args.get('site_name', None),
            request.args.get('type', None)
        ]
        cursor.execute(sql, args)
        result = cursor.fetchall()
        return result

"""
post username, transit_type, transit_route, date

Return None
"""
def _s36_log_transit(conn):
    with conn.cursor() as cursor:
        sql = f'call take_transit(%s, %s, %s, %s)'
        data = request.get_json()
        args = [
            data.get('username', None),
            data.get('type', None),
            data.get('route', None),
            data.get('date', None)
        ]
        cursor.execute(sql, args)
    conn.commit()

"""
Return site_name, open_everyday, address (address + zipcode)
"""
def _s37_view_site(conn):
    with conn.cursor() as cursor:
        sql = f'call view_site(%s)'
        args = [request.args.get('site_name', None)]
        cursor.execute(sql, args)
        result = cursor.fetchall()
        return result

"""
post username, site_name, date

Return None
"""
def _s37_log_visit_site(conn):
    with conn.cursor() as cursor:
        sql = f'call log_visit_site(%s, %s, %s)'
        data = request.get_json()
        args = [
            data.get('username', None),
            data.get('site_name', None),
            data.get('date', None)
                ]
        cursor.execute(sql, args)
    conn.commit()

"""
Return visit_date, event_name, site_name, price

"""
def _s38_filter_visits(conn):
    with conn.cursor() as cursor:
        sql = f'call filter_visits(%s, %s, %s, %s, %s)'
        args = [
            session.get('username'),
            request.args.get('event_name', None),
            request.args.get('site_name', None),
            request.args.get('start_date', None),
            request.args.get('end_date', None)
        ]
        cursor.execute(sql, args)
        results = cursor.fetchall()
        for i in range(len(results)):
            results[i]['price'] = float(results[i]['price'])

        return results
