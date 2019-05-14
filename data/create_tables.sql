drop database if exists cs4400_team70;
create database cs4400_team70;
use cs4400_team70;


CREATE TABLE user
(
    username   VARCHAR(15) NOT NULL,
    password   CHAR(224) NOT NULL,
    status     VARCHAR(15) NOT NULL,
    first_name VARCHAR(15) NOT NULL,
    last_name  VARCHAR(15) NOT NULL,
    PRIMARY KEY (username)
) ENGINE = INNODB;


CREATE TABLE user_email
(
    username VARCHAR(15) NOT NULL,
    email    VARCHAR(50) NOT NULL,
    PRIMARY KEY (email),
    FOREIGN KEY (username) REFERENCES user (username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    UNIQUE (email)
) ENGINE = INNODB;


CREATE TABLE visitor
(
    username varchar(15) not null,
    primary key (username),
    foreign key (username) REFERENCES user (username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = INNODB;


CREATE TABLE employee
(
    username   VARCHAR(15) NOT NULL,
    employeeID VARCHAR(15),
    phone      VARCHAR(12) NOT NULL,
    address    VARCHAR(30) NOT NULL,
    city       VARCHAR(20) NOT NULL,
    state      VARCHAR(15)  NOT NULL,
    zipcode    VARCHAR(15)     NOT NULL,
    PRIMARY KEY (username),
    UNIQUE (phone),
    FOREIGN KEY (username) REFERENCES user (username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = INNODB;


CREATE TABLE administrator
(
    username VARCHAR(15) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES employee (username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = INNODB;


CREATE TABLE staff
(
    username VARCHAR(15) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES employee (username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = INNODB;


CREATE TABLE manager
(
    username VARCHAR(15) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES employee (username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = INNODB;


CREATE TABLE site
(
    name             VARCHAR(30) NOT NULL,
    address          VARCHAR(30),
    zipcode          VARCHAR(15)     NOT NULL,
    open_everyday    int         NOT NULL,
    manager_username VARCHAR(15) NOT NULL,
    PRIMARY KEY (name),
    FOREIGN KEY (manager_username) REFERENCES manager (username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    UNIQUE (manager_username)
) ENGINE = INNODB;


CREATE TABLE event
(
    event_name    VARCHAR(50)   NOT NULL,
    start_date    DATE          NOT NULL,
    site_name     VARCHAR(30)   NOT NULL,
    end_date      DATE          NOT NULL,
    price         DECIMAL(5, 2) NOT NULL DEFAULT 0,
    capacity      INT           NOT NULL,
    min_staff_req INT           NOT NULL,
    description   TEXT,
    PRIMARY KEY (event_name, start_date, site_name),
    FOREIGN KEY (site_name) REFERENCES site (name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = INNODB;


CREATE TABLE transit
(
    type  VARCHAR(15)   NOT NULL,
    route VARCHAR(15)   NOT NULL,
    price DECIMAL(5, 2) NOT NULL,
    PRIMARY KEY (type, route)
) ENGINE = INNODB;


CREATE TABLE assign_to
(
    staff_username VARCHAR(15) NOT NULL,
    event_name     VARCHAR(50) NOT NULL,
    start_date     DATE        NOT NULL,
    site_name      VARCHAR(30) NOT NULL,
    PRIMARY KEY (event_name, start_date, staff_username, site_name),
    FOREIGN KEY (event_name, start_date, site_name) REFERENCES event (event_name, start_date, site_name)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (staff_username) REFERENCES staff (username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = INNODB;


CREATE TABLE take_transit
(
    username VARCHAR(15) NOT NULL DEFAULT "deleted",
    type     VARCHAR(15) NOT NULL,
    route    VARCHAR(15) NOT NULL,
    date     DATE        NOT NULL,
    PRIMARY KEY (date, username, type, route),
    FOREIGN KEY (username) REFERENCES user (username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (type, route) REFERENCES transit (type, route)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = INNODB;


CREATE TABLE connect
(
    site_name VARCHAR(30) NOT NULL,
    type      VARCHAR(15) NOT NULL,
    route     VARCHAR(15) NOT NULL,
    PRIMARY KEY (type, route, site_name),
    FOREIGN KEY (type, route) REFERENCES transit (type, route)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (site_name) REFERENCES site (name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = INNODB;


CREATE TABLE visit_site
(
    username  VARCHAR(15) NOT NULL DEFAULT "deleted",
    site_name VARCHAR(30) NOT NULL,
    date      DATE        NOT NULL,
    PRIMARY KEY (date, username, site_name),
    FOREIGN KEY (username) REFERENCES visitor (username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (site_name) REFERENCES site (name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = INNODB;


CREATE TABLE visit_event
(
    username   VARCHAR(15) NOT NULL DEFAULT "deleted",
    event_name VARCHAR(50) NOT NULL,
    start_date DATE        NOT NULL,
    site_name  VARCHAR(30) NOT NULL,
    date       DATE        NOT NULL,
    PRIMARY KEY (date, username, event_name, start_date, site_name),
    FOREIGN KEY (username) REFERENCES visitor (username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (event_name, start_date, site_name) REFERENCES event (event_name, start_date, site_name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = INNODB;



