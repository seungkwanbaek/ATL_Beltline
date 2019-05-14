use cs4400_team70;
delimiter //

-- Screen 1: User Login

create procedure user_login(in in_email varchar(50), in_pwd varchar(15))
begin
    select username, status from user natural join user_email where email = in_email and password = SHA2(in_pwd, 224);
end //

-- Screen 3: Register User Only

create procedure add_user (in username varchar(15), password varchar(15), firstname varchar(15), lastname varchar(15))
begin
    insert into user(username, password, status, first_name, last_name) values (username, SHA2(password, 224), "Pending", firstname, lastname);
end //

create procedure add_email(in username varchar(15), email varchar(50))
begin
    insert into user_email(username, email) values (username, email);
end //

-- Screen 4: Register Visitor Only

create procedure add_visitor(in username varchar(15))
begin
    insert into visitor(username) values (username);
end //

-- Screen 5: Register Employee Only

create procedure add_employee(in username varchar(15), phone varchar(12), address varchar(30), city varchar(20), state varchar(15), zipcode varchar(5))
begin
    insert into employee(username, employeeID, phone, address, city, state, zipcode) values (username, NULL, phone, address, city, state, zipcode);
end //

create procedure add_manager(in username varchar(15))
begin
    insert into manager(username) values (username);
end //

create procedure add_staff (in username varchar(15))
begin
    insert into staff(username) values (username);
end //

-- Screen 6: Register Employee-Visitor Only
-- Use defined procedures.

-- Screen 15: User Take Transit

create procedure take_transit(in username varchar(15), type varchar(15), route varchar(15), date date)
begin
    insert into take_transit(username, type, route, date) values (username, type, route, date);
end //

create procedure get_site_names()
begin
    select name as site_name from site;
end //





#######################################################################################
create procedure take_transit_filter(in in_type varchar(15), in_site varchar(30), low_price decimal(5,2), high_price decimal(5,2))
begin
select t.type, t.route, count(site_name) as connected_sites, price from connect c natural join transit t
    where (t.type, t.route) in (select connect.type, route from connect where in_site is NULL OR site_name = in_site)
    and (in_type is NULL OR in_type = type)
    and (low_price is NULL OR price >= low_price)
    and (high_price is NULL OR price <= high_price)
        group by t.type, t.route;
end //

-- Screen 16: User Take History

create procedure filter_transit_history(in in_type varchar(15), in_site varchar(30), in_route varchar(15), in_start_date date, in_end_date date, in_username varchar(15))
begin
    select distinct type, route, date, price from take_transit natural join transit natural join connect
    where (in_type is NULL OR in_type = 'ALL' or in_type = type)
    and (in_site is NULL OR in_site = site_name)
    and (in_route is NULL OR in_route = route)
    and (in_start_date is NULL OR date >= in_start_date)
    and (in_end_date is NULL OR date <= in_end_date)
    and in_username = username;
end //

-- Screen 17: Employee Manage Profile
create procedure get_employee_profile(in in_username varchar(15))
begin
    select first_name, last_name, username, site.name as site_name, employeeID, phone, concat(employee.address, ', ', city, ', ', state, ' ', employee.zipcode) as 'address'
    from employee natural JOIN user LEFT JOIN site ON site.manager_username = username
    where username = in_username;
end //

create procedure update_profile_employee(in in_username varchar(15), in_firstname varchar(15), in_lastname varchar(15), in_phone varchar(12))
begin
    UPDATE user SET first_name = in_firstname, last_name = in_lastname where username = in_username;
    UPDATE employee SET phone = in_phone where username = in_username;
end //

create procedure delete_visitor (in in_username varchar(15))
begin
    DELETE from visitor where username = in_username;
end //

create procedure delete_event (in in_event_name varchar(50), in in_site_name varchar(30), in in_start_date Date)
begin
    delete from event where event_name = in_event_name and site_name = in_site_name and start_date = in_start_date;
end //

create procedure delete_site (in in_site_name varchar(30))
begin
    delete from site where name = in_site_name;
end //

create procedure  delete_transit(in in_type varchar(15), in in_route varchar(15))
begin
    delete from transit where type = in_type and route = in_route;
end //

create procedure delete_email (in in_email varchar(50))
begin
    DELETE from user_email where email = in_email;
end //

-- Screen 18: Administrator Manage User

create procedure filter_user(in in_username varchar(15), in_status varchar(15), in_user_type varchar(15))
begin
    IF in_user_type = "Visitor" THEN
        select username from user where username in
            (select username from user where in_status is null or status = in_status)
        and username in
            (select username from user where in_username is null or username = in_username)
        and username in
            (select username from visitor);
    ELSEIF in_user_type = "Employee" THEN
        select username from user where username in
            (select username from user where in_status is null or status = in_status)
        and username in
            (select username from user where in_username is null or username = in_username)
        and username in
            (select username from employee);
    ELSEIF in_user_type = "Administrator" THEN
        select username from user where username in
            (select username from user where in_status is null or status = in_status)
        and username in
            (select username from user where in_username is null or username = in_username)
        and username in
            (select username from administrator);
    ELSEIF in_user_type = "Staff" THEN
        select username from user where username in
            (select username from user where in_status is null or status = in_status)
        and username in
            (select username from user where in_username is null or username = in_username)
        and username in
            (select username from staff);
    ELSEIF in_user_type = "Manager" THEN
        select username from user where username in
            (select username from user where in_status is null or status = in_status)
        and username in
            (select username from user where in_username is null or username = in_username)
        and username in
            (select username from manager);
    ELSE
        select username from user where username in
            (select username from user where in_status is null or status = in_status)
        and username in
            (select username from user where in_username is null or username = in_username);
    END IF;
end //

create procedure get_status_by_username(in in_username varchar(15))
begin
    select status from user where username = in_username;
end //

create procedure get_num_emails(in in_username varchar(15))
begin
    select count(*) as number_emails from user_email group by username having username = in_username;
end //

create procedure update_status(in in_username varchar(15), in_new_status varchar(15), in_employeeID varchar(15))
begin
    update employee set employeeID = in_employeeID where in_username = username;
    UPDATE user set status = in_new_status where in_username = username;
end //

-- Screen 19: Administrator Manage Site
create procedure admin_get_site_detail(in in_site_name varchar(30))
begin
    select name as site_name, zipcode, address, open_everyday, manager_username from site where name = in_site_name;
end //

create procedure get_manager_usernames_and_names()
begin
    select username, CONCAT(first_name, ' ', last_name) as fullname from user where username in (select username from manager);
end //

create procedure get_site_and_open_everyday(in in_manager_username varchar(15))
begin
    select name as site_name, open_everyday from site where manager_username = in_manager_username;
end //
create procedure filter_sites(in in_site_name varchar(30), in_manager_username varchar(15), in_open_everyday int)
begin
    select name as site_name, manager_username, open_everyday from site
    where (in_site_name is NULL OR in_site_name = name)
    and (in_open_everyday is NULL OR in_open_everyday = open_everyday)
    and (in_manager_username is NULL OR manager_username = in_manager_username);
end //

create procedure get_manager_name(in in_manager_username varchar(15))
begin
    select concat(first_name, ' ', last_name) as fullname from user where username = in_manager_username;
end //

-- Screen 20: Administrator Edit Site

create procedure edit_site(in in_site_name varchar(30), in_address varchar(30), in_zipcode varchar(15), in_open_everyday int, in in_old_site_name varchar(30), in_username varchar(15))
begin
    UPDATE site SET name = in_site_name, address = in_address, zipcode = in_zipcode, open_everyday = in_open_everyday, manager_username = in_username
    where name = in_old_site_name;
end //

create procedure show_all_managers_not_assigned_and_current_manager (in in_site_name varchar(30))
begin
    select concat(first_name, ' ', last_name) as fullname, username from user
    where username in (select username from manager
    where username NOT IN (select site.manager_username from site) OR
    username = (select manager_username from site where site.name = in_site_name));
end //

-- Screen 21: Administrator Create Site

create procedure create_site(in in_site_name varchar(30), in_address varchar(30), in_zipcode varchar(15), in_manager_username varchar(15), in_open_everyday int)
begin
    insert into site(name, address, zipcode, open_everyday, manager_username) values (in_site_name, in_address, in_zipcode, in_open_everyday, in_manager_username);
end //

create procedure show_all_managers_not_assigned()
begin
    select username, concat(first_name, " ", last_name) as fullname from user
    where username in (select username from manager
    where username NOT in (select manager_username from site));
end //

-- Screen 22: Administrator Manage Transit

create procedure filter_transit_as_administrator(in in_type varchar(15), in in_route varchar(15), in in_site varchar(50), in low_price decimal(5,2), in high_price decimal(5,2))
begin
    select route, type, price from transit where (in_type is NULL OR in_type = type)
    and (in_site is NULL OR in_site in (select site_name from connect where (in_type is NULL or type = in_type) and (in_route is NULL OR in_route = route)))
    and (in_route is NULL OR in_route = route)
    and (low_price is NULL OR price >= low_price)
    and (high_price is NULL OR price <= high_price);
end //

create procedure get_num_connected_sites(in in_type varchar(15), in_route varchar(15))
begin
    select count(*) as number_connected from connect where type = in_type and route = in_route;
end //

create procedure get_num_transit_logged(in in_type varchar(15), in_route varchar(15))
begin
    select count(*) as number_logged from take_transit where in_type = type and in_route = route;
end //

-- Screen 23: Administrator Edit Transit

create procedure update_transit(in new_route varchar(15), old_route varchar(15), in_price decimal(5,2))
begin
    if new_route = old_route then
        UPDATE transit set price = in_price where route = old_route;
    else
        UPDATE transit set price = in_price, route = new_route where route = old_route;
    end if;
end //

create procedure add_transit_connection(in in_type varchar(15), in_route varchar(15), in_site_name varchar(30))
begin
    insert into connect(type, route, site_name) values (in_type, in_route, in_site_name);
end //

create procedure remove_transit_connection(in in_type varchar(15), in_route varchar(15), in_site_name varchar(30))
begin
    delete from connect where type = in_type and route = in_route and site_name = in_site_name;
end //

create procedure show_current_connected_sites(in in_type varchar(15), in_route varchar(15))
begin
    select site_name from connect where type = in_type and route = in_route ORDER BY site_name;
end //

-- Screen 24: Administrator Create Transit

create procedure create_transit (in in_type varchar(15), in_route varchar(15), in_price decimal(5,2))
begin
    insert into transit (type, route, price) values (in_type, in_route, in_price);
end //

-- Screen 25: Manager Manage Event

create procedure get_visits_for_event(in in_event_name varchar(50), in in_site_name varchar(30), in in_start_date Date)
begin
    select count(*) as number_visits from visit_event where event_name = in_event_name and site_name = in_site_name and start_date = in_start_date;
end //

create procedure get_revenue_for_event(in in_event_name varchar(50), in in_site_name varchar(30), in in_start_date Date)
begin
    select count(*) * price as revenue from event natural join visit_event group by event_name, site_name, start_date having event_name = in_event_name and site_name = in_site_name and start_date = in_start_date;
end //

create procedure get_site_name_for_manager (in in_manager_username varchar(15))
begin
    select name as site_name from site where manager_username = in_manager_username;
end //

create procedure get_events_within_duration_for_site(in in_duration_low int, in in_duration_high int, in in_site_name varchar(30))
begin
    select event_name, site_name, start_date from event where abs(datediff(start_date, end_date)) between in_duration_low and in_duration_high and site_name = in_site_name;
end //

create procedure get_events_in_visit_range_for_site(in in_visit_low int, in in_visit_high int, in in_site_name varchar(30))
begin
    select event_name, site_name, start_date from visit_event group by event_name, site_name, start_date having count(*) between in_visit_low and in_visit_high and site_name = in_site_name;
end //

create procedure get_events_within_revenue_range_for_site(in in_revenue_low int, in in_revenue_high int, in in_site_name varchar(30))
begin
    select event_name, site_name, start_date
    from (select event_name, site_name, start_date, price * count(*) as revenue
            from visit_event natural join event
            group by event_name, site_name, start_date
            having revenue between in_revenue_low and in_revenue_high and site_name = in_site_name) as t;
end //

create procedure get_event_staff_count(in in_event_name varchar(50), in in_site_name varchar(50), in in_start_date Date)
begin
    select count(*) as number_staff from assign_to where event_name = in_event_name and start_date = in_start_date and site_name = in_site_name;
end //

-- Screen 26: Manager View/Edit Event

create procedure get_all_attributes_for_event(in in_event_name varchar(50), in in_site_name varchar(30), in in_start_date Date)
begin
    select * from event where event_name = in_event_name and site_name = in_site_name and start_date = in_start_date;
end //

create procedure get_assigned_staff_for_event(in in_event_name varchar(50), in in_site_name varchar(30), in in_start_date date)
begin
    select username, CONCAT(first_name, ' ', last_name) as fullname from user where username in
        (select staff_username as username from assign_to where event_name = in_event_name and start_date = in_start_date and site_name = in_site_name);
end //

create procedure get_available_staff_for_time_range(in in_event_start_date Date, in_event_end_date date)
begin
    select username, CONCAT(first_name, ' ', last_name) as fullname from user where username in (select username from staff) and username not in
    (select distinct staff_username as username from assign_to natural join event where start_date between in_event_start_date and in_event_end_date
    or event.end_date between in_event_start_date and in_event_end_date);
end //

create procedure get_daily_visits_for_event(in in_event_name varchar(50), in in_site_name varchar(30), in in_start_date Date, in in_event_date Date)
begin
    select count(*) as number_visits from visit_event where site_name = in_site_name
    and event_name = in_event_name
    and start_date = in_start_date
    and date = in_event_date;
end //

create procedure get_daily_revenue_for_event(in in_event_name varchar(50), in in_site_name varchar(50), in in_start_date Date, in in_event_date Date)
begin
    select price * count(*) as revenue from
    visit_event natural join event where event_name = in_event_name and site_name = in_site_name and start_date = in_start_date
    and date = in_event_date group by event_name, site_name, start_date;
end //

create procedure unassign_staff_for_event(in in_staff_username varchar(15), in in_event_name varchar(50), in in_site_name varchar(30), in in_start_date Date)
begin
    DELETE from assign_to where in_staff_username = staff_username
    and event_name = in_event_name
    and in_site_name = site_name
    and in_start_date = start_date;
end //

-- Screen 27: Manager Create Event

create procedure add_new_event (in event_name varchar(50), start_date DATE, end_date DATE, price decimal(5,2), capacity INT, min_staff INT, description TEXT, site_name varchar(30))
begin
    insert into event (event_name, start_date, site_name, end_date, price, capacity, description, min_staff_req) values (event_name, start_date, site_name, end_date, price, capacity, description, min_staff);
end //

create procedure display_all_available_staff (in in_start_date DATE, in_end_date DATE)
begin
    select username, concat(first_name, ' ', last_name) as fullname
    from user
    where username in (
        select staff_username from
            (select count(*) as fullcount, staff_username
                from event natural join assign_to
                group by staff_username) n
            natural join
            (select count(*) as partialcount, staff_username
                from event natural join assign_to
                    where NOT (in_start_date <= end_date and start_date <= in_end_date)
                group by staff_username) m
        where partialcount = fullcount
    );
end //

create procedure assign_staff (in in_username varchar(15),  in_event_name varchar(50), in_site_name varchar(30), in_start_date DATE)
begin
    insert into assign_to (staff_username, event_name, start_date, site_name) values (in_username, in_event_name, in_start_date, in_site_name);
end //

-- Screen 28: Manager Manage Staff

create procedure filter_staff(in in_site_name varchar(30), in in_first_name varchar(15), in in_last_name varchar(15))
begin
    select username, concat(first_name, ' ', last_name) as fullname from user where username IN (select username from staff)
    and (in_first_name is NULL OR first_name = in_first_name)
    and (in_last_name is NULL OR last_name = in_last_name)
    and (in_site_name is NULL OR username in (select username from assign_to where site_name = in_site_name));
end //

create procedure get_number_of_shifts_for_staff(in in_staff_username varchar(15), in in_start_date Date, in in_end_date Date, in in_site_name varchar(30))
begin
    select count(*) as number_shifts from assign_to natural JOIN event where staff_username = in_staff_username
    and (in_start_date is NULL OR start_date >= in_start_date)
    and (in_end_date is NULL OR end_date <= in_end_date)
    and (in_site_name is null OR site_name = in_site_name);
end //

-- Screen 29: Manager Site Report

create procedure get_event_count_for_site_on_date(in in_date Date, in in_site_name varchar(30))
begin
    select count(*) as number_events from event
    where in_date BETWEEN start_date and end_date
    and site_name = in_site_name;
end //

create procedure get_staff_count_for_site_on_date(in in_date Date, in in_site_name varchar(30))
begin
    select count(*) as number_staff from
        (select distinct staff_username from assign_to natural JOIN event where site_name = in_site_name and in_date BETWEEN start_date and end_date) as t;
end //

create procedure get_visits_for_site_on_date(in in_date Date, in in_site_name varchar(30))
begin
    select count(*) as number_visits from visit_site where site_name = in_site_name and date = in_date;
end //

create procedure get_visits_for_event_at_site_on_date(in in_date Date, in in_site_name varchar(30))
begin
    select count(*) as number_visits from visit_event natural join event where date = in_date and site_name = in_site_name;
end //

create procedure get_visits_for_event_at_site_between_date(in in_start_date Date, in in_end_date Date, in in_site_name varchar(30))
begin
    select count(*) as number_visits from visit_event natural join event where date between in_start_date and in_end_date and site_name = in_site_name;
end //

create procedure get_visits_for_site_between_date(in in_start_date Date, in in_end_date Date, in in_site_name varchar(30))
begin
    select count(*) as number_visits from visit_site where date between
                                                           in_start_date and
                                                           in_end_date and
                                                           site_name =
                                                           in_site_name;
end //

create procedure get_revenue_for_site_on_date(in in_date Date, in in_site_name varchar(30))
begin
    select sum(revenue) as revenue from
    (select price * count(*) as revenue from visit_event join event
    where event.site_name = in_site_name and in_date = date
     group by event.event_name, event.site_name, event.start_date) as t;
end //

-- Screen 30: Manager Daily Detail

create procedure show_event (in in_username varchar(50), in_curr_date DATE)
begin
    select event_name, count(*) as visits, count(*) * price as revenue from event natural join visit_event
        where date = in_curr_date and site_name = (select name as site_name from site where site.manager_username = in_username)
    group by event_name;
end //

create procedure get_events_for_site_on_date(in in_site_name varchar(30), in in_date Date)
begin
    select event_name, site_name, start_date from event where site_name = in_site_name
    and in_date between start_date and end_date;
end //

create procedure staff_that_day_at_site (in in_username varchar(15), in_curr_date date)
begin
    select event_name, concat(first_name, ' ', last_name) as fullname
    from event natural join assign_to join user on user.username = assign_to.staff_username
        where site_name = (select name as site_name from site where manager_username = in_username)
          and in_curr_date between start_date and end_date order by fullname;
end //

-- Screen 31: Staff View Schedule

create procedure filter_assigned_event_for_staff(in in_staff_username varchar(15), in in_start_date Date, in in_end_date Date, in in_event_name varchar(50), in in_keyword varchar(15))
begin
    select event_name, site_name, start_date, end_date from event JOIN site ON event.site_name = site.name
    where (in_start_date is NULL OR event.start_date >= in_start_date)
    and (in_end_date is NULL OR event.end_date <= in_end_date)
    and (in_event_name is NULL OR event.event_name = in_event_name)
    and (in_keyword is NULL OR event.description LIKE CONCAT('%', in_keyword,'%'))
    and ((start_date, site_name, event_name) IN (select start_date, site_name, event_name from assign_to where staff_username = in_staff_username));
end //

create procedure get_number_of_staff_assigned_for_event(in in_event_name varchar(50), in in_site_name varchar(30), in in_start_date Date)
begin
    select count(*) as number_staff from assign_to where in_event_name = event_name and in_start_date = start_date and in_site_name = site_name;
end //

-- Screen 32: Staff Event Detail

create procedure get_event_duration(in in_event_name varchar(50), in in_site_name varchar(30), in in_start_date Date)
begin
    select datediff(end_date, start_date) as duration from event where event_name = in_event_name and site_name = in_site_name and start_date = in_start_date;
end //

create procedure staff_event_detail (in in_event_name varchar(50), in_site_name varchar(30), in_start_date DATE)
begin
    select event_name, site_name, start_date, end_date, DATEDIFF(end_date, start_date) as duration, capacity, price, description from event
        where event_name = in_event_name and start_date = in_start_date and site_name = in_site_name;
end //

create procedure staff_assigned_to_event (in in_event_name varchar(50), in_site_name varchar(30), in_start_date DATE)
begin
    select username, concat(first_name, ' ', last_name) as fullname from user
        where username in (select staff_username from assign_to
                      where event_name = in_event_name
                        and site_name = in_site_name
                        and start_date = in_start_date)
    ORDER BY fullname;
end //

-- Screen 33: Visitor Explore Event

create procedure get_capacity_for_event(in in_event_name varchar(50), in_site_name varchar(30), in_start_date date)
begin
    select capacity from event where event_name = in_event_name and site_name = in_site_name and start_date = in_start_date;
end //

create procedure get_my_visits_for_event(in in_visitor_username varchar(15), in_event_name varchar(50), in_site_name varchar(30), in_start_date date)
begin
    select count(*) as number_visits from visit_event where username = in_visitor_username and event_name = in_event_name and site_name = in_site_name and start_date = in_start_date;
end //

create procedure get_event_visits(in in_site_name varchar(30), in_event_name varchar(50), in_event_start_date date)
begin
    select count(*) as number_visits from visit_event where event_name = in_event_name and start_date = in_event_start_date and site_name = in_site_name;
end //

create procedure get_events_in_visit_range(in in_visit_low int, in_visit_high int)
begin
    select site_name, start_date, event_name from visit_event GROUP BY site_name, start_date, event_name HAVING count(*) BETWEEN in_visit_low and in_visit_high;
end //

create procedure get_events_in_price_range(in in_price_low Decimal(5,2), in_price_high Decimal(5,2))
begin
    select site_name, start_date, event_name from event where price BETWEEN in_price_low and in_price_high;
end //

create procedure get_events_visited(in in_visitor_username varchar(15))
begin
    select event_name, site_name, start_date from visit_event where username = in_visitor_username;
end //

create procedure get_sold_out_events()
begin
    select event_name, site_name, start_date, COUNT(*)
    from visit_event natural JOIN event
    GROUP BY event_name, site_name, start_date, capacity HAVING capacity = COUNT(*);
end //

create procedure get_events_with_name(in in_event_name varchar(50))
begin
    select event_name, site_name, start_date from event where event_name = in_event_name;
end //

create procedure get_events_for_site(in in_site_name varchar(30))
begin
    select event_name, site_name, start_date from event where site_name = in_site_name;
end //

create procedure get_events_with_keyword(in in_keyword varchar(15))
begin
    select event_name, site_name, start_date from event where description LIKE CONCAT('%', in_keyword, '%');
end //

create procedure get_events_between_dates(in in_start_date date, in_end_date date)
begin
    select event_name, site_name, start_date from event
    where (in_start_date is NULL OR start_date >= in_start_date)
     and (in_end_date is NULL OR end_date <= in_end_date);
end //

create procedure get_price_for_event(in in_event_name varchar(50), in in_site_name varchar(30), in in_start_date Date)
begin
    select price from event where event_name = in_event_name and site_name = in_site_name and start_date = in_start_date;
end //

-- Screen 34: Visitor Event Detail

create procedure visitor_view_event (in in_event_name varchar(50), in_site_name varchar(30), in_start_date DATE)
begin
    select event_name, site_name, start_date, end_date, price,
           (capacity - (select COUNT(*) from visit_event where visit_event.event_name = in_event_name and visit_event.start_date = in_start_date and visit_event.site_name = in_site_name)) as 'tickets_remaining',
           description
    from event where event_name = in_event_name and site_name = in_site_name and start_date = in_start_date;
end //

create procedure log_visit_event (in in_username varchar(15), in_event_name varchar(50), in_site_name varchar(30), in_start_date DATE, in_curr_date DATE)
begin
    insert into visit_event (username, event_name, start_date, site_name, date) values (in_username, in_event_name, in_start_date, in_site_name, in_curr_date);
end //

-- Screen 35: Visitor Explore Site

create procedure get_visits_for_site_between_dates(in in_site_name varchar(30), in in_start_date Date, in in_end_date Date)
begin
    select count(*) from visit_site where site_name = in_site_name and visit_site_date BETWEEN in_start_date and in_end_date;
end //

create procedure get_my_visits_for_events_at_site_between_dates(in
in_site_name varchar(30), in in_visitor_username varchar(15), in in_start_date Date, in in_end_date Date)
begin
    select count(*) as number_visits from visit_event where site_name = in_site_name and date BETWEEN in_start_date and in_end_date and username = in_visitor_username;
end //

create procedure get_my_visits_for_site_between_dates(in in_site_name varchar(30), in in_visitor_username varchar(15), in in_start_date Date, in in_end_date Date)
begin
    select count(*) as number_visits from visit_site where username = in_visitor_username and (in_start_date is null or in_end_date is null or date between in_start_date and in_end_date) and site_name = in_site_name;
end //


create procedure get_site_by_includes_visited(in in_visitor_username varchar(15))
begin
    select distinct site_name from visit_site where username = in_visitor_username;
end //

-- changed_Bryan

create procedure get_site_by_event_count_between_dates(in in_start_date Date, in in_end_date Date, in in_event_number_low int, in in_event_number_high int)
begin
    select site_name from
        (select name as site_name, count(*) as event_number from site JOIN
          event ON event.site_name = site.name where in_start_date <=
                                                     end_date and in_end_date
                                                                  >=
                                                                  start_date
        group by name) as t
    where event_number BETWEEN in_event_number_low and in_event_number_high;
end //

-- HERE

create procedure get_event_count_between_dates(in in_start_date Date, in in_end_date Date, in in_site_name varchar(30))
begin
    select count(*) as number_events from event where site_name = in_site_name and (in_start_date is null or end_date is null or (in_start_date <= end_date and in_end_date >= start_date));
end //

create procedure get_site_by_visit_range_between_dates(in in_start_date Date, in in_end_date Date, in in_visits_low int, in in_visits_high int)
begin
    select distinct site_name, sum(visits) as visits from
        ((select site_name, count(*) as visits from visit_site
          where date BETWEEN in_start_date and in_end_date GROUP BY site_name)
         union
         (select site_name, count(*) as visits from visit_event
          where date BETWEEN in_start_date and in_end_date GROUP BY site_name)) as t
    group by site_name
    having sum(visits) between in_visits_low and in_visits_high;
end //

create procedure get_site_by_open_everyday()
begin
    select name as site_name from site where open_everyday = 1;
end //

create procedure get_site_by_open_everyday_specific(in in_open_everyday int)
begin
    select name as site_name from site where open_everyday = in_open_everyday;
end //

create procedure get_site_by_name(in in_site_name varchar(30))
begin
    select name as site_name from site where name = in_site_name;
end //

-- Screen 36: Visitor Transit Detail
# create procedure get_transit_by_type(in in_type varchar(15))
# begin
#     select type, route from transit where in_type is NULL or type = in_type;
# end //
#
# create procedure get_transit_by_site(in in_site varchar(15))
# begin
#     select type, route from connect where site_name = in_site;
# end //
#
# create procedure filter_transit(in in_site varchar(30), in in_type varchar(15))
# begin
#     select type, route from transit where (in_type is null or type = in_type) and (type, route) in (select type, route from connect where site_name = in_site);
#   end //

create procedure filter_transit_by_site_type(in in_site_name varchar(30), in_type varchar(15))
begin
    select route, type, price from transit where (in_type is null or type = in_type)
    and (type, route) in (select type, route from connect where site_name = in_site_name);
end //

create procedure get_transit_information(in in_site varchar(15), in in_type
    varchar(15))
begin
    select type, route, price, count(*) as connected_sites from connect
    natural JOIN transit
    where (type, route) in (select type, route from transit where (in_type is null or type = in_type) and (type, route) in (select type, route from connect where site_name = in_site))
    group by transit.type, transit.route;
end //

-- Screen 37: Visitor Site Detail

create procedure view_site(in in_site_name varchar(30))
begin
    select name as site_name, open_everyday, concat(address, ' ', zipcode) as address
    from site where name = in_site_name;
end //

create procedure log_visit_site (in in_username varchar(15), in in_site_name VARCHAR(30), in in_date DATE)
begin
    insert into visit_site (username, site_name, date) VALUE (in_username, in_site_name, in_date);
end //

-- Screen 38: Visitor Visit History

# create procedure filter_visits_by_event_name(in in_event_name varchar(50), in in_visitor_username varchar(15))
# begin
#     select date, event_name, site_name, price from visit_event natural join event where event_name = in_event_name and username = in_visitor_username;
# end //
#
# create procedure filter_visits_by_site(in in_site_name varchar(30), in in_visitor_username varchar(15))
# begin
#     (select date, event_name, site_name, price from visit_event natural join event where site_name = in_site_name and username = in_visitor_username)
#     union
#     (select date, null as event_name, site_name, 0 as price from visit_site where site_name = in_site_name and username = in_visitor_username);
# end //
#
# create procedure filter_visits_by_date_range(in in_start_date Date, in in_end_date date, in in_visitor_username varchar(15))
# begin
#     (select date, event_name, site_name, price from visit_event natural JOIN event where username = in_visitor_username and (in_start_date is null or date >= in_start_date) and (in_end_date is null or date <= in_end_date))
#     union
#     (select date, null as event_name, site_name, 0 as price from visit_site where username = in_visitor_username and (in_start_date is null or date >= in_start_date) and (in_end_date is null or date <= in_end_date));
# end //

create procedure filter_visits(in in_visitor_username varchar(15), in in_event_name varchar(50), in in_site_name varchar(30), in in_start_date Date, in in_end_date Date)
begin
    select distinct date, event_name, site_name, price from
    (select username, date, event_name, site_name, price from visit_event natural join event
    union
    select username, date, null as event_name, site_name, 0 as price from visit_site) as t
    where t.username = in_visitor_username
    and (in_event_name is null or t.event_name = in_event_name)
    and (in_site_name is null or t.site_name = in_site_name)
    and (in_start_date is null or t.date >= in_start_date)
    and (in_end_date is null or t.date <= in_end_date);
end //

delimiter ;
