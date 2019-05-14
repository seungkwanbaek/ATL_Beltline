from functools import wraps

from flask import session, jsonify


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify('not logged in'), 401

        return f(*args, **kwargs)
    return wrap


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('type') == 'administrator':
            return jsonify("api not available for current user type"), 401

        return f(*args, **kwargs)

    return wrap


def manager_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('type') == 'manager':
            return jsonify("api not available for current user type"), 401

        return f(*args, **kwargs)
    return wrap


def staff_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('type') == 'staff':
            return jsonify("api not available for current user type"), 401

        return f(*args, **kwargs)

    return wrap


def employee_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('is_employee'):
            return jsonify("api not available for current user type"), 401

        return f(*args, **kwargs)

    return wrap


def visitor_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('is_visitor'):
            return jsonify("api not available for current user type"), 401

        return f(*args, **kwargs)

    return wrap
