import datetime

import pymysql
from flask import session, request, jsonify
from backend.dbconn import create_connection
import random


def for_testing():

    conn = create_connection()

    try:
        result = _s25_filter_events(conn)

        return jsonify(result), 200
    except Exception as err:
        return jsonify(err.__str__()), 400
    finally:
        conn.close()
    return jsonify('fucked up'),  400


# returns date, route, type, price of transport meeting filters
def _s16_filter_transit_history(conn, filters):
    with conn.cursor() as cursor:
        sql = f'call filter_transit_history(%s, %s, %s, %s, %s, %s)'
        args = [filters.get('transport_type'),
                filters.get('site_name'),
                filters.get('route'),
                filters.get('start_date'),
                filters.get('end_date'),
                session['username']]
        cursor.execute(sql, args)

        result = cursor.fetchall()
        return result


# returns first name, last name, username, site name (if manager, null otherwise), empID, phone,
# address of an employee username
def _s17_get_fields_for_employee(conn, params):
    with conn.cursor() as cursor:
        sql = f'call get_employee_profile(%s)'
        args = [params.get('employee_username')]
        cursor.execute(sql, args)

        result = cursor.fetchall()
        return result


# returns a list of user names that meet the filters
def _s18_get_usernames_by_filter(conn):
    with conn.cursor() as cursor:
        sql = f'call filter_user(%s, %s, %s)'
        args = [
            request.args.get('username', None),
            request.args.get('status', None),
            request.args.get('user_type', None)
        ]

        cursor.execute(sql, args)

        result = cursor.fetchall()
        return result


# returns number of emails and status for user names
def _s18_get_information_for_tables(conn):
    usernames = _s18_get_usernames_by_filter(conn)

    result = []
    with conn.cursor() as cursor:
        for row in usernames:
            username = row['username']
            args = [username]
            status_sql = f'call get_status_by_username(%s)'
            emails_sql = f'call get_num_emails(%s)'
            cursor.execute(status_sql, args)
            status = cursor.fetchone()['status']

            cursor.execute(emails_sql, args)
            number_emails = cursor.fetchone()['number_emails']
            result.append({"status": status,
                           "number_emails": number_emails,
                           "username": row['username']})
    return result


# updates the status of a user
def _s18_update_user_status(conn):
    with conn.cursor() as cursor:
        sql = f'call update_status(%s, %s, %s)'
        data = request.get_json()
        print(data.get('new_status'))
        args = [
            data.get('username'),
            data.get('new_status'),
            generate_employee_id()
        ]
        cursor.execute(sql, args)
    conn.commit()


def _s19_populate_sites(conn):
    with conn.cursor() as cursor:
        sql = f'call get_site_names()'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def _s19_populate_managers(conn):
    with conn.cursor() as cursor:
        sql = f'call get_manager_usernames_and_names()'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


# returns name of site, manager_username, open_everyday
def _s19_filter_sites(conn):
    with conn.cursor() as cursor:
        sql = f'call filter_sites(%s, %s, %s)'
        args = [
            request.args.get('site_name'),
            request.args.get('username'),
            request.args.get('open_everyday')
        ]

        cursor.execute(sql, args)
        result = cursor.fetchall()
        result = _s19_populate_table(conn, result)
        return result

def _s19_populate_table(conn, result):
    with conn.cursor() as c:
        for i in range(len(result)):
            sql = 'call get_site_and_open_everyday(%s)'
            c.execute(sql, (result[i]['manager_username'],))
            q = c.fetchone()
            result[i]['site_name'] = q['site_name']
            result[i]['open_everyday'] = q['open_everyday']
    return result


# returns full name of manager for all sites
def _s19_get_manager_names_for_sites(conn):
    sites = _s19_filter_sites(conn)
    with conn.cursor() as cursor:
        for i in range(len(sites)):
            manager_username = sites[i]['manager_username']
            sql = f'call get_manager_name(%s)'
            args = [manager_username]

            cursor.execute(sql, args)
            manager_name = cursor.fetchone()['fullname']
            sites[i]['fullname'] = manager_name
    return sites


def _s19_delete_site(conn):
    with conn.cursor() as c:
        sql = f'call delete_site(%s)'
        c.execute(sql, (request.args.get('site_name'),))
    conn.commit()


def _s20_get_unassigned_manager_names(conn):
    with conn.cursor() as cursor:
        sql = f'call show_all_managers_not_assigned()'
        cursor.execute(sql)

        results = cursor.fetchall()
    return results


def _s20_get_manager_names(conn):
    return _s19_populate_managers(conn)


def _s20_get_site_info(conn):
    with conn.cursor() as c:
        sql = f'call admin_get_site_detail(%s)'
        c.execute(sql, (request.args.get('site_name'),))
        row = c.fetchone()

        sql = f'call get_manager_name(%s)'
        c.execute(sql, (row['manager_username'],))
        name = c.fetchone()
        row['fullname'] = name['fullname']
    return row


def _s20_edit_site(conn):
    with conn.cursor() as cursor:
        sql = f'call edit_site(%s, %s, %s, %s, %s, %s)'
        data = request.get_json()

        args = [
            data.get('site_name'),
            data.get('address'),
            data.get('zipcode'),
            data.get('open_everyday'),
            data.get('old_site_name'),
            data.get('manager_username')
        ]

        cursor.execute(sql, args)
    conn.commit()





def _s21_create_site(conn):
    with conn.cursor() as cursor:
        sql = f'call create_site(%s, %s, %s, %s, %s)'
        data = request.get_json()
        args = [
            data.get('site_name'),
            data.get('address'),
            data.get('zipcode'),
            data.get('manager_username'),
            data.get('open_everyday')
        ]
        cursor.execute(sql, args)

    conn.commit()


def _s22_populate_sites(conn):
    return _s19_populate_sites(conn)


# returns route, type, price
def _s22_filter_transit(conn):
    with conn.cursor() as cursor:
        sql = f'call filter_transit_as_administrator(%s, %s, %s, %s, %s)'
        args = [
            request.args.get('type'),
            request.args.get('route'),
            request.args.get('site_name'),
            request.args.get('low_price'),
            request.args.get('high_price')
        ]

        cursor.execute(sql, args)
        result = cursor.fetchall()
        return result


def _s22_get_info_for_table(conn):
    transits = _s22_filter_transit(conn)

    with conn.cursor() as cursor:
        for i in range(len(transits)):
            row = transits[i]
            route = row['route']
            type = row['type']
            args = [type, route]
            num_sites_sql = f'call get_num_connected_sites(%s, %s)'
            num_logged_sql = f'call get_num_transit_logged(%s, %s)'

            cursor.execute(num_logged_sql, args)
            num_logged = cursor.fetchone()['number_logged']
            cursor.execute(num_sites_sql, args)
            num_connected = cursor.fetchone()['number_connected']

            row["number_logged"] = num_logged
            row["number_connected"] = num_connected
            row['price'] = float(row['price'])
    return transits


def _s22_delete_transit(conn):
    data = request.get_json()
    with conn.cursor() as c:
        sql = f'call delete_transit(%s, %s)'
        c.execute(sql, (request.args.get('type'), request.args.get('route')))
    conn.commit()


def _s23_get_connected_sites(conn):
    with conn.cursor() as cursor:
        sql = f'call show_current_connected_sites(%s, %s)'
        args = [
            request.args.get('type'),
            request.args.get('route')
        ]
        cursor.execute(sql, args)
        result = cursor.fetchall()
        return result


def _s23_get_all_sites(conn):
    return _s19_populate_sites(conn)


def _s23_update_transit_info(conn):
    with conn.cursor() as c:
        sql = f'call update_transit(%s, %s, %s)'
        data = request.get_json()
        args = [
            data.get('route'),
            data.get('old_route'),
            data.get('price')
        ]

        c.execute(sql, args)

    conn.commit()


def _s23_remove_connected_sites(conn, sites_to_remove):
    with conn.cursor() as c:
        sql = f'call remove_transit_connection(%s, %s, %s)'
        c.executemany(sql, sites_to_remove)
    conn.commit()


def _s23_add_connected_sites(conn, sites_to_add):
    with conn.cursor() as c:
        sql = f'call add_transit_connection(%s, %s, %s)'
        c.executemany(sql, sites_to_add)
    conn.commit()


def _s24_get_all_sites(conn):
    return _s19_populate_sites(conn)


def _s24_create_transit(conn):
    with conn.cursor() as c:
        sql = f'call create_transit(%s, %s, %s)'
        data = request.get_json()
        args = [
            data.get('type'),
            data.get('route'),
            data.get('price')
        ]
        c.execute(sql, args)
    conn.commit()
    to_add = [(data.get('type'), data.get('route'), site) for site in data.get('sites')]
    _s24_add_connected_sites(conn, to_add)


def _s24_add_connected_sites(conn, data):
    _s23_add_connected_sites(conn, data)


def _s25_get_site_for_manager(conn):
    with conn.cursor() as c:
        sql = f'call get_site_name_for_manager(%s)'
        args = [session['username']]

        c.execute(sql, args)
        result = c.fetchone()

        return result


def _s25_filter_events(conn):
    results = []
    with conn.cursor() as c:
        event_name = request.args.get('event_name', None)
        keyword = request.args.get('keyword', None)
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        low_duration = request.args.get('low_duration', None)
        high_duration = request.args.get('high_duration', None)
        low_visit = request.args.get('low_visits', None)
        high_visit = request.args.get('high_visits', None)
        low_revenue = request.args.get('low_revenue', None)
        high_revenue = request.args.get('high_revenue', None)
        site_name = session.get('site_name', None)

        if event_name:
            sql = f'call get_events_with_name(%s)'
            c.execute(sql, (event_name,))
            rows = c.fetchall()
            result = []
            for row in rows:
                result.append((row['event_name'], row['site_name'], row['start_date']))
            results.append(result)
        if keyword:
            sql = f'call get_events_with_keyword(%s)'
            c.execute(sql, (keyword,))
            rows = c.fetchall()
            result = []
            for row in rows:
                result.append((row['event_name'], row['site_name'], row['start_date']))
            results.append(result)
        if start_date or end_date:
            sql = f"call get_events_between_dates(%s, %s)"

            args = [
                request.args.get('start_date'),
                request.args.get('end_date')
            ]
            c.execute(sql, args)
            rows = c.fetchall()
            result = []
            for row in rows:
                result.append((row['event_name'], row['site_name'], row['start_date']))
            results.append(result)
        if low_duration or high_duration:
            if not low_duration:
                low_duration = 0
            if not high_duration:
                high_duration = 999999999
            sql = f'call get_events_within_duration_for_site(%s, %s, %s)'
            c.execute(sql, (low_duration, high_duration, site_name))
            rows = c.fetchall()
            result = []

            for row in rows:
                result.append((row['event_name'], row['site_name'], row['start_date']))
            results.append(result)
        if low_visit or high_visit:
            if not low_visit:
                low_visit = 0
            if not high_visit:
                high_visit = 999999999
            sql = f'call get_events_in_visit_range_for_site(%s, %s, %s)'
            c.execute(sql, (low_visit, high_visit, site_name))
            rows = c.fetchall()

            result = []
            for row in rows:
                result.append((row['event_name'], row['site_name'], row['start_date']))
            results.append(result)
        if low_revenue or high_revenue:
            if not low_revenue:
                low_revenue = 0
            if not high_revenue:
                high_revenue = 999999999
            sql = f'call get_events_within_revenue_range_for_site(%s, %s, %s)'
            c.execute(sql, (low_revenue, high_revenue, site_name))
            rows = c.fetchall()
            result = []
            for row in rows:
                result.append((row['event_name'], row['site_name'], row['start_date']))
            results.append(result)
        sql = f'call get_events_for_site(%s)'
        c.execute(sql, (site_name,))
        rows = c.fetchall()
        result = []
        for row in rows:
            result.append((row['event_name'], row['site_name'], row['start_date']))
        results.append(result)
        final_result = list(set(results[0]))
        if len(results) > 1:
            for i in range(1, len(results)):
                final_result = list(set(final_result) & set(results[i]))

        return_set = []
        for row in final_result:
            return_set.append({"event_name": row[0], "site_name": row[1], "start_date": row[2]})
        return return_set


def _s25_filter_event_get_attributes(conn):
    event_keys = _s25_filter_events(conn)

    with conn.cursor() as c:
        for event in event_keys:
            args = list(event.values())
            sql = 'call get_event_staff_count(%s,%s,%s)'
            c.execute(sql, args)
            event['number_staff'] = c.fetchone()['number_staff']

            sql = 'call get_revenue_for_event(%s,%s,%s)'
            c.execute(sql, args)
            revenue = c.fetchone()
            if revenue is None:
                event['revenue'] = 0
            else:
                event['revenue'] = float(revenue['revenue'])

            sql = 'call get_visits_for_event(%s,%s,%s)'
            c.execute(sql, args)
            event['number_visits'] = c.fetchone()['number_visits']

            sql = 'call get_event_duration(%s,%s,%s)'
            c.execute(sql, args)
            event['duration'] = c.fetchone()['duration']
    return event_keys


def _s25_delete_event(conn):
    with conn.cursor() as c:
        sql = f'call delete_event(%s, %s, %s)'
        c.execute(sql, (request.args.get('event_name'), session.get('site_name'), request.args.get('start_date')))
    conn.commit()


def _s26_get_event_information(conn):
    with conn.cursor() as c:
        sql = f'call get_all_attributes_for_event(%s, %s, %s)'
        args = [
            request.args.get('event_name'),
            session.get('site_name'),
            request.args.get('start_date')
        ]

        c.execute(sql, args)
        result = c.fetchone()
        if result is not None:
            result['price'] = float(result['price'])
        return result


def _s26_get_available_staff(conn, start_date, end_date):
    with conn.cursor() as c:
        sql = f'call get_available_staff_for_time_range({start_date}, {end_date})'
        c.execute(sql)
        result = c.fetchall()
        return result


def _s26_get_assigned_staff(conn):
    with conn.cursor() as c:
        sql = f'call get_assigned_staff_for_event(%s, %s, %s)'
        args = [
            request.args.get('event_name'),
            session.get('site_name'),
            request.args.get('start_date')
        ]
        c.execute(sql, args)
        result = c.fetchall()
        return result


def _s26_get_daily_details(conn):
    site_name = session.get('site_name')
    event_name = request.args.get('event_name')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    start = [int(el) for el in start_date.split('-')]
    end = [int(el) for el in end_date.split('-')]
    d1 = datetime.date(start[0], start[1], start[2])
    d2 = datetime.date(end[0], end[1], end[2])
    delta = d2 - d1
    dates = []
    for i in range(delta.days + 1):
        dates.append(str(d1 + datetime.timedelta(i)))

    results = []
    with conn.cursor() as c:
        visits_sql = f'call get_daily_visits_for_event(%s, %s, %s, %s)'
        revenue_sql = f'call get_daily_revenue_for_event(%s, %s, %s, %s)'
        for date in dates:
            args = [event_name, site_name, start_date, date]
            c.execute(visits_sql, args)
            visits = c.fetchone()['number_visits']

            c.execute(revenue_sql, args)
            res = c.fetchone()
            if res is None:
                revenue = 0
            else:
                revenue = float(res['revenue'])

            results.append({"date": date, "number_visits": visits, "revenue": revenue})

    return results


def _s26_remove_assignments(conn, staff_to_remove):
    with conn.cursor() as c:
        sql = f'call unassign_staff_for_event(%s, %s, %s, %s)'
        c.executemany(sql, staff_to_remove)
    conn.commit()


def _s26_add_assignments(conn, staff_to_add):
    with conn.cursor() as c:
        sql = f'call assign_staff(%s, %s, %s, %s)'
        c.executemany(sql, staff_to_add)
    conn.commit()


def _s26_update_event_description(conn):
    data = request.get_json()

    with conn.cursor() as c:
        sql = f'update event set description = %s where event_name = %s and site_name = %s and start_date = %s'
        args = [
            data.get('description'),
            data.get('event_name'),
            session.get('site_name'),
            data.get('start_date')
        ]
        c.execute(sql, args)
    conn.commit()


def _s27_create_event(conn):
    data = request.get_json()
    with conn.cursor() as c:
        sql = f'call add_new_event(%s, %s, %s, %s, %s, %s, %s, %s)'
        args = [
            data.get('event_name'),
            data.get('start_date'),
            data.get('end_date'),
            data.get('price'),
            data.get('capacity'),
            data.get('min_staff_req'),
            data.get('description'),
            session.get('site_name')
        ]
        c.execute(sql, args)
    conn.commit()

    event_keys = [data.get('event_name'), session.get('site_name'), data.get('start_date')]
    staffs = [[staff, *event_keys] for staff in data.get('staff')]

    _s27_assign_staff_to_event(conn, staffs)


def _s27_get_available_staff(conn):
    with conn.cursor() as c:
        sql = f'call display_all_available_staff(%s, %s)'
        args = [
            request.args.get('start_date', None),
            request.args.get('end_date', None)
        ]

        c.execute(sql, args)
        result = c.fetchall()
        return result


def _s27_assign_staff_to_event(conn, staff_to_add):
    _s26_add_assignments(conn, staff_to_add)



def _s28_get_site_names(conn):
    return _s19_populate_sites(conn)



def _s28_filter_staff(conn):
    with conn.cursor() as c:
        sql = f'call filter_staff(%s, %s, %s)'
        args =[
            session.get('site_name'),
            request.args.get('first_name', None),
            request.args.get('last_name', None)
        ]

        c.execute(sql, args)
        result = c.fetchall()
        return result


def _s28_get_event_shifts(conn):
    staff = _s28_filter_staff(conn)

    with conn.cursor() as c:
        for person in staff:
            sql = f'call get_number_of_shifts_for_staff(%s, %s, %s, %s)'
            args = [
                person['username'],
                request.args.get('start_date', None),
                request.args.get('end_date', None),
                session.get('site_name')
            ]
            c.execute(sql, args)
            person.update(c.fetchone())
    return staff


def _s29_filter_daily_details(conn):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    start = [int(el) for el in start_date.split('-')]
    end = [int(el) for el in end_date.split('-')]
    d1 = datetime.date(start[0], start[1], start[2])
    d2 = datetime.date(end[0], end[1], end[2])
    delta = d2 - d1
    dates = []
    for i in range(delta.days + 1):
        dates.append(str(d1 + datetime.timedelta(i)))

    low_event = request.args.get('low_event', None)
    high_event = request.args.get('high_event', None)
    low_staff = request.args.get('low_staff', None)
    high_staff = request.args.get('high_staff', None)
    low_visits = request.args.get('low_visits', None)
    high_visits = request.args.get('high_visits', None)
    low_revenue = request.args.get('low_revenue', None)
    high_revenue = request.args.get('high_revenue', None)
    site_name = session.get('site_name')
    results = []
    with conn.cursor() as c:
        for date in dates:

            event_sql = f'call get_event_count_for_site_on_date(%s, %s)'
            staff_sql = f'call get_staff_count_for_site_on_date(%s, %s)'
            site_visits_sql = f'call get_visits_for_site_on_date(%s, %s)'
            event_visits_sql = f'call get_visits_for_event_at_site_on_date(%s, %s)'
            revenue_sql = f'call get_revenue_for_site_on_date(%s, %s)'
            args = [date, site_name]

            c.execute(event_sql, args)
            num_events = int(c.fetchone()['number_events'])
            if not low_event:
                low_event = 0
            if not high_event:
                high_event = 999999999
            if num_events > int(high_event) or num_events < int(low_event):
                continue

            c.execute(staff_sql, args)
            num_staff = int(c.fetchone()['number_staff'])
            if not low_staff:
                low_staff = 0
            if not high_staff:
                high_staff = 999999999
            if num_staff < int(low_staff) or num_staff > int(high_staff):
                continue

            c.execute(site_visits_sql, args)
            num_site_visits = int(c.fetchone()['number_visits'])
            c.execute(event_visits_sql, args)
            num_event_visits = int(c.fetchone()['number_visits'])
            total_visits = num_event_visits + num_site_visits
            if not low_visits:
                low_visits = 0
            if not high_visits:
                high_visits = 999999999
            if total_visits < int(low_visits) or total_visits > int(high_visits):
                continue

            c.execute(revenue_sql, args)
            res = c.fetchone()
            if res.get('revenue'):
                revenue = float(res.get('revenue'))
            else:
                revenue = 0

            if not low_revenue:
                low_revenue = 0
            if not high_revenue:
                high_revenue = 999999999
            if revenue < float(low_revenue) or revenue > float(high_revenue):
                continue

            results.append({"date": date, "number_events": num_events, "number_staff": num_staff, "number_visits":
                           total_visits, "revenue": revenue})
        return results


def _s30_get_events_for_site_on_date(conn):
    with conn.cursor() as c:
        sql = f'call get_events_for_site_on_date(%s, %s)'
        args = [
            session.get('site_name'),
            request.args.get('date', None)
        ]

        c.execute(sql, args)
        result = c.fetchall()
        return result


def _s30_populate_table(conn):
    events = _s30_get_events_for_site_on_date(conn)
    with conn.cursor() as c:
        for i in range(len(events)):
            event = events[i]
            staff_sql = f'call get_assigned_staff_for_event(%s, %s, %s)'
            args = [
                event['event_name'],
                event['site_name'],
                event['start_date']
            ]
            c.execute(staff_sql, args)
            staff_result = c.fetchall()
            assigned_staff = []
            for row in staff_result:
                assigned_staff.append(row['fullname'])

            visits_sql = f'call get_daily_visits_for_event(%s, %s, %s, %s)'
            args.append(request.args.get('date'))
            c.execute(visits_sql, args)
            visits = c.fetchone()['number_visits']

            revenue_sql = f'call get_daily_revenue_for_event(%s, %s, %s, %s)'
            c.execute(revenue_sql, args)
            res = c.fetchone()
            if res is None:
                revenue = 0
            else:
                revenue = float(res['revenue'])

            event["staff"] = assigned_staff
            event['number_visits'] = visits
            event["revenue"] = float(revenue)
        return events


def _s31_filter_events(conn):
    with conn.cursor() as c:
        sql = f'call filter_assigned_event_for_staff(%s, %s, %s, %s, %s)'
        args = [
            session['username'],
            request.args.get('start_date', None),
            request.args.get('end_date', None),
            request.args.get('event_name', None),
            request.args.get('keyword', None)
        ]

        c.execute(sql, args)
        result = c.fetchall()
        return result


def _s31_get_staff_counts(conn):
    events = _s31_filter_events(conn)
    with conn.cursor() as c:

        for i in range(len(events)):
            sql = f'call get_number_of_staff_assigned_for_event(%s, %s, %s)'
            args = [
                events[i]['event_name'],
                events[i]['site_name'],
                events[i]['start_date']
            ]
            c.execute(sql, args)
            # result = c.fetchone()
            # print(result['count(*)'])
            num_staff = c.fetchone()['number_staff']
            events[i]['number_staff'] = num_staff

    return events


# main
def _s32_view_staff_detail(conn):
    with conn.cursor() as c:
        sql = f'call staff_event_detail(%s, %s, %s)'
        args = [
            request.args.get('event_name'),
            request.args.get('site_name'),
            request.args.get('start_date')
        ]
        c.execute(sql, args)
        result = c.fetchone()
        if result is not None:
            result['price'] = float(result['price'])

    result = _s32_get_staff_assigned(conn, result)
    return result


def _s32_get_staff_assigned(conn, result):
    with conn.cursor() as c:
        sql = f'call staff_assigned_to_event(%s, %s, %s)'
        args = [
            request.args.get('event_name'),
            request.args.get('site_name'),
            request.args.get('start_date')
        ]

        c.execute(sql, args)
        staff_assigned = []
        query_result = c.fetchall()
        for row in query_result:
            staff_assigned.append(row['fullname'])
    result['staff'] = staff_assigned

    return result


# main
def _s33_filter_events(conn):
    event_name = request.args.get('event_name', None)
    keyword = request.args.get('keyword', None)
    site_name = request.args.get('site_name', None)
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    low_visit = request.args.get('low_visits', None)
    high_visit = request.args.get('high_visits', None)
    low_price = request.args.get('low_price', None)
    high_price = request.args.get('high_price', None)

    results = []
    with conn.cursor() as c:
        if event_name:
            sql = f'call get_events_with_name(%s)'
            c.execute(sql, (event_name,))
            rows = c.fetchall()
            result = []
            for row in rows:
                result.append((row['event_name'], row['site_name'], row['start_date']))
            results.append(result)
        if keyword:
            sql = f'call get_events_with_keyword(%s)'
            c.execute(sql, (keyword,))
            rows = c.fetchall()
            result = []
            for row in rows:
                result.append((row['event_name'], row['site_name'], row['start_date']))
            results.append(result)
        if site_name:
            sql = f'call get_events_for_site(%s)'
            c.execute(sql, (site_name,))
            rows = c.fetchall()
            result = []
            for row in rows:
                result.append((row['event_name'], row['site_name'], row['start_date']))
            results.append(result)
        if start_date or end_date:
            sql = f'call get_events_between_dates(%s, %s)'
            args = [
                start_date, end_date
            ]
            c.execute(sql, args)
            rows = c.fetchall()
            result = []
            for row in rows:
                result.append((row['event_name'], row['site_name'], row['start_date']))
            results.append(result)
        if low_visit or high_visit:
            if not low_visit:
                low_visit = 0
            if not high_visit:
                high_visit = 999999999
            sql = f'call get_events_in_visit_range(%s, %s)'
            args = [low_visit, high_visit]
            c.execute(sql, args)
            rows = c.fetchall()
            result = []
            for row in rows:
                result.append((row['event_name'], row['site_name'], row['start_date']))
            results.append(result)
        if low_price or high_price:
            if not low_price:
                low_price = 0
            if not high_price:
                high_price = 999
            sql = f'call get_events_in_price_range(%s, %s)'
            args = [low_price, high_price]
            c.execute(sql, args)
            rows = c.fetchall()
            result = []
            for row in rows:
                result.append((row['event_name'], row['site_name'], row['start_date']))
            results.append(result)

    with conn.cursor() as c:
        sql = 'select event_name, site_name, start_date from event'
        c.execute(sql)
        rows = c.fetchall()
        result = []
        for row in rows:
            result.append((row['event_name'], row['site_name'], row['start_date']))
        results.append(result)

    final_result = []
    if len(results):
        if len(results) > 1:
            final_result = list(set(results[0]))
            for i in range(1, len(results)):
                final_result = list(set(final_result) & set(results[i]))
        else:
            final_result = list(set(results[0]))

    return_set = []

    for row in final_result:
        return_set.append({"event_name": row[0], "site_name": row[1], "start_date": row[2]})

    return_set = _s33_populate_table(conn, return_set)
    return return_set


def _s33_populate_sites(conn):
    return _s19_populate_sites(conn)


def _s33_populate_table(conn, return_set):
    with conn.cursor() as c:
        for i in range(len(return_set)):
            event_name = return_set[i]['event_name']
            site_name =  return_set[i]['site_name']
            start_date =  return_set[i]['start_date']

            price_sql = f'call get_price_for_event(%s, %s, %s)'
            capacity_sql = f'call get_capacity_for_event(%s, %s, %s)'
            visits_sql = f'call get_visits_for_event(%s, %s, %s)'
            my_visits_sql =f'call get_my_visits_for_event(%s, %s, %s, %s)'

            args = [event_name, site_name, start_date]
            c.execute(price_sql, args)
            price = float(c.fetchone()['price'])
            c.execute(capacity_sql, args)
            capacity = int(c.fetchone()['capacity'])
            c.execute(visits_sql, args)
            visits = int(c.fetchone()['number_visits'])
            args = [session.get('username'), event_name, site_name, start_date]
            c.execute(my_visits_sql, args)
            my_visits = int(c.fetchone()['number_visits'])
            remaining = capacity - visits

            return_set[i]["price"] = price
            return_set[i]["tickets_remaining"] = remaining
            return_set[i]["number_visits"] = visits
            return_set[i]["my_visits"] = my_visits
    return return_set


def _s35_populate_sites(conn):
    return _s19_populate_sites(conn)


def _s35_filter_sites(conn):
    open_everyday = request.args.get('open_everyday', None)
    site_name = request.args.get('site_name', None)
    start_date = request.args.get('start_date', '1999-01-01')
    end_date = request.args.get('end_date', '2024-01-01')
    low_visit = request.args.get('low_visits', 0)
    high_visit = request.args.get('high_visits', 99999999)
    low_event = request.args.get('low_event', 0)
    high_event = request.args.get('high_event', 9999999)

    results = []
    with conn.cursor() as c:
        if site_name:
            sql = f'call get_site_by_name(%s)'
            c.execute(sql, (site_name,))
            rows = c.fetchall()
            result = []
            for row in rows:
                result.append((row['site_name'],))
            results.append(result)
        if open_everyday:
            sql = f'call get_site_by_open_everyday_specific(%s)'
            c.execute(sql, (open_everyday,))
            rows = c.fetchall()
            result = []
            for row in rows:
                result.append((row['site_name'],))
            results.append(result)
        sql = f'call get_site_by_visit_range_between_dates(%s, %s, %s, %s)'
        args = [start_date, end_date, low_visit, high_visit]
        c.execute(sql, args)
        rows = c.fetchall()
        result = []
        for row in rows:
            result.append((row['site_name'],))
        results.append(result)

        sql = f'call get_site_by_event_count_between_dates(%s, %s, %s, %s)'
        args = [start_date, end_date, low_event, high_event]
        c.execute(sql, args)
        rows = c.fetchall()
        result = []
        for row in rows:
            result.append((row['site_name'],))
        results.append(result)
        final_result = []
        if len(results):
            if len(results) > 1:
                final_result = list(set(results[0]))
                for i in range(1, len(results)):
                    final_result = list(set(final_result) & set(results[i]))
            else:
                final_result = list(set(results[0]))

        return_set = []

        for row in final_result:
            return_set.append({"site_name": row[0]})

        return_set = _s35_populate_tables(conn, return_set, start_date, end_date)
        return return_set


def _s35_populate_tables(conn, return_set, start_date, end_date):
    with conn.cursor() as c:
        for i in range(len(return_set)):
            site_name = return_set[i]['site_name']
            event_sql = f'call get_event_count_between_dates(%s, %s, %s)'
            args = [start_date, end_date, site_name]
            c.execute(event_sql,args)
            event_count = c.fetchone()['number_events']

            event_visit_sql = f'call get_visits_for_event_at_site_between_date(%s, %s, %s)'
            site_visit_sql = f'call get_visits_for_site_between_date(%s, %s, %s)'
            args = [start_date, end_date, site_name]
            c.execute(event_visit_sql, args)
            event_visit = c.fetchone()['number_visits']
            c.execute(site_visit_sql, args)
            site_visit = c.fetchone()['number_visits']
            total_visits = int(event_visit) + int(site_visit)

            my_site_sql = f'call get_my_visits_for_site_between_dates(%s, %s, %s, %s)'
            my_event_sql = f'call ' \
                           f'get_my_visits_for_events_at_site_between_dates(%s, %s, %s, %s)'
            args = [site_name, session.get('username'), start_date, end_date]
            c.execute(my_site_sql, args)
            my_site = c.fetchone()['number_visits']

            c.execute(my_event_sql, args)
            my_event = c.fetchone()['number_visits']
            my_total = int(my_site) + int(my_event)
            return_set[i]['number_events'] = event_count
            return_set[i]['number_visits'] = total_visits
            return_set[i]['my_visits'] = my_total
    return return_set


def _s36_populate_table_with_filter(conn):
    with conn.cursor() as c:
        sql = f'call filter_transit_by_site_type(%s, %s)'
        args = [
            request.args.get('site_name'),
            request.args.get('type')
        ]
        c.execute(sql, args)
        results = c.fetchall()
        for i in range(len(results)):
            t_route = results[i]['route']
            t_type = results[i]['type']
            results[i]['price'] = float(results[i]['price'])

            sql = f'call get_num_connected_sites(%s, %s)'
            args = [t_type, t_route]
            c.execute(sql, args)

            result = c.fetchone()['number_connected']
            results[i]['number_connected'] = result

    return results


def _s36_log_transit(conn):
    with conn.cursor() as c:
        sql = f'call take_transit(%s, %s, %s, %s)'
        data = request.get_json()
        args = [
            session.get('username'),
            data.get('type'),
            data.get('route'),
            data.get('date')
        ]
        c.execute(sql, args)
    conn.commit()


def _s37_get_site_detail(conn):
    with conn.cursor() as c:
        sql = f'call view_site(%s)'
        c.execute(sql, (request.args.get('site_name'),))
        return c.fetchone()


def _s37_log_site_visit(conn):
    with conn.cursor() as c:
        data = request.get_json()
        sql = f'call log_visit_site(%s, %s, %s)'
        args = [
            session.get('username'),
            data.get('site_name'),
            data.get('date')
        ]
        c.execute(sql, args)
    conn.commit()


def generate_employee_id():
    return str(random.randint(1, 800000000) + 100000000)

