from flask import Flask,  render_template

from backend import login, visitor, user, administrator, manager, staff

from datetime import date

from flask.json import JSONEncoder

from backend import account
from backend import alans_procedures
from backend.request_filters import login_required, staff_required, employee_required, admin_required, manager_required, \
    visitor_required


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()

        return super().default(o)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.secret_key = 'very secret key'


@app.route("/", methods=['GET'])
def main():
    return render_template('1_User_Login.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    return login.login()


@app.route('/api/logout', methods=['DELETE'])
def api_logout():
    return login.logout()


@app.route('/api/site/manager', methods=['GET'])
@login_required
@manager_required
def site_name_as_manager():
    return manager.get_site_name()


@app.route('/api/register', methods=['POST'])
def register():
    return account.register()


@app.route('/api/transit/log', methods=['POST'])
@login_required
def take_transit():
    return user.take_transit()


@app.route('/api/transit/user/filter', methods=['GET'])
@login_required
def filter_transits():
    return user.filter_transits()


@app.route('/api/site', methods=['GET'])
@login_required
def all_sites():
    return user.get_all_sites()


@app.route('/api/transit/types', methods=['GET'])
@login_required
def all_transport_types():
    return user.get_all_transport_types()


@app.route('/api/transit/history', methods=['GET'])
@login_required
def filter_transit_history():
    return user.filter_transit_history()


@app.route('/api/profile', methods=['GET'])
@login_required
@employee_required
def get_employee_profile():
    return account.get_employee_profile()


@app.route('/api/profile', methods=['PUT'])
@login_required
@employee_required
def update_employee_profile():
    return account.update_employee_profile()


# Administrator
@app.route('/api/user/statuses', methods=['GET'])
@login_required
@admin_required
def filter_manage_user():
    return administrator.filter_manage_user()


@app.route('/api/user/change_status', methods=['PUT'])
@login_required
@admin_required
def change_user_status():
    return administrator.update_user_status()


@app.route('/api/user/managers', methods=['GET'])
@login_required
@admin_required
def get_all_managers():
    return administrator.get_managers()


@app.route('/api/user/managers/available', methods=['GET'])
@login_required
@admin_required
def get_unassigned_managers():
    return administrator.get_unassigned_managers()


# Site
@app.route('/api/site/new', methods=['POST'])
@login_required
@admin_required
def create_site():
    return administrator.create_site()


@app.route('/api/site/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_site():
    return administrator.delete_site()


@app.route('/api/site/show', methods=['GET'])
@login_required
@admin_required
def show_site():
    return administrator.get_site_info()


@app.route('/api/site/update', methods=['PUT'])
@login_required
@admin_required
def update_site():
    return administrator.update_site()


@app.route('/api/site/meta', methods=['GET'])
@login_required
@admin_required
def filter_manage_site():
    return administrator.filter_manage_site()


# Transit
@app.route('/api/transit/new', methods=['POST'])
@login_required
@admin_required
def create_transit():
    return administrator.create_transit()


@app.route('/api/transit/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_transit():
    return administrator.delete_transit()


@app.route('/api/transit/update', methods=['PUT'])
@login_required
@admin_required
def update_transit():
    return administrator.update_transit()


@app.route('/api/transit/filter', methods=['GET'])
@login_required
@admin_required
def filter_manage_transit():
    return administrator.filter_manage_transit()


@app.route('/api/transit/sites', methods=['GET'])
@login_required
@admin_required
def connected_sites():
    return administrator.transit_connected_sites()


# Manager
# Event
@app.route('/api/event/manager/filter', methods=['GET'])
@login_required
@manager_required
def filter_manage_event():
    return manager.filter_manage_event()


@app.route('/api/event/new', methods=['POST'])
@login_required
@manager_required
def create_event():
    return manager.create_event()


@app.route('/api/event/show', methods=['GET'])
@login_required
@manager_required
def show_event():
    return manager.get_event_info()


@app.route('/api/event/daily/filter', methods=['GET'])
@login_required
@manager_required
def daily_event_report():
    return manager.daily_event_info()


@app.route('/api/event/delete', methods=['DELETE'])
@login_required
@manager_required
def delete_event():
    return manager.delete_event()


@app.route('/api/event/update', methods=['PUT'])
@login_required
@manager_required
def update_event():
    return manager.update_event()


@app.route('/api/staff/available', methods=['GET'])
@login_required
@manager_required
def manager_get_available_staff():
    return manager.get_available_staff()


@app.route('/api/user/staff/filter', methods=['GET'])
@login_required
@manager_required
def manager_filter_staff():
    return manager.filter_staff()


@app.route('/api/site/report', methods=['GET'])
@login_required
@manager_required
def filter_site_report():
    return manager.filter_site_report()


@app.route('/api/site/report/daily', methods=['GET'])
@login_required
@manager_required
def site_daily_report():
    return manager.daily_site_report()


# Staff
@app.route('/api/staff/schedule', methods=['GET'])
@login_required
@staff_required
def staff_schedule():
    return staff.filter_schedule()


@app.route('/api/staff/schedule/details', methods=['GET'])
@login_required
@staff_required
def staff_schedule_details():
    return staff.schedule_details()


# Visitor
@app.route('/api/event/visitor/filter', methods=['GET'])
@login_required
@visitor_required
def explore_event():
    return visitor.filter_explore_event()


@app.route('/api/event/visitor/details', methods=['GET'])
@login_required
@visitor_required
def event_details():
    return visitor.event_detail()


@app.route('/api/event/log', methods=['POST'])
@login_required
@visitor_required
def event_visit():
    return visitor.log_event_visit()


@app.route('/api/site/filter', methods=['GET'])
@login_required
@visitor_required
def explore_site():
    return visitor.filter_explore_site()


@app.route('/api/site/details', methods=['GET'])
@login_required
@visitor_required
def site_details():
    return visitor.get_site_details()


@app.route('/api/site/log', methods=['POST'])
@login_required
@visitor_required
def site_visit():
    return visitor.log_site_visit()


@app.route('/api/transit/details', methods=['GET'])
@login_required
@visitor_required
def transit_details():
    return visitor.get_transit_details()


@app.route('/api/transit/log', methods=['POST'])
@login_required
@visitor_required
def transit_visit():
    return visitor.log_transit_visit()


@app.route('/api/visitor/history', methods=['GET'])
@login_required
@visitor_required
def visit_history():
    return visitor.visit_history()


