CREATE SCHEMA `job_worksheets` ;

USE job_worksheets;

CREATE TABLE status (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    status TEXT
);

INSERT INTO status (status) VALUES ("Open");
INSERT INTO status (status) VALUES ("Closed");

CREATE TABLE resource (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name TEXT ,
    rate INTEGER,
    mobile_phone TEXT,
    note TEXT
);

INSERT INTO resource (name, rate) VALUES ("Super Dump", 120);
INSERT INTO resource (name, rate) VALUES ("End Dump", 130);
INSERT INTO resource (name, rate) VALUES ("Side Dump", 120);
INSERT INTO resource (name, rate) VALUES ("Transfer", 95);
INSERT INTO resource (name, rate) VALUES ("Conestoga", 120);
INSERT INTO resource (name, rate) VALUES ("4 Axle", 85);
INSERT INTO resource (name, rate) VALUES ("High Track Dozer", 75);
INSERT INTO resource (name, rate) VALUES ("Bobcat", 100);
INSERT INTO resource (name, rate) VALUES ("Parking Lot", 50.5);
INSERT INTO resource (name, rate) VALUES ("Low Boy", 50.5);
INSERT INTO resource (name, rate) VALUES ("Roller", 50);
INSERT INTO resource (name, rate) VALUES ("160 Excavator", 50);
INSERT INTO resource (name, rate) VALUES ("75 Excavator", 50);
INSERT INTO resource (name, rate) VALUES ("Mini Excavator", 50);
INSERT INTO resource (name, rate) VALUES ("Dozer", 50);
INSERT INTO resource (name, rate) VALUES ("Compactor", 50);
INSERT INTO resource (name, rate) VALUES ("Pump", 50);
INSERT INTO resource (name, rate) VALUES ("Cody", 100);
INSERT INTO resource (name, rate) VALUES ("Tony", 100);
INSERT INTO resource (name, rate) VALUES ("Kerry", 100);
INSERT INTO resource (name, rate) VALUES ("David", 100);
INSERT INTO resource (name, rate) VALUES ("Gene", 100);
INSERT INTO resource (name, rate) VALUES ("Ditch Digger", 75);
INSERT INTO resource (name, rate) VALUES ("Flagger", 55);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name TEXT,
    address INTEGER,
    notes TEXT
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name TEXT,
    customer_id INTEGER,
    date_open DATE,
    date_close DATE,
    status_id INTEGER,
    location TEXT,
    notes TEXT
);

CREATE TABLE worksheets (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    jobs_id TEXT,
    date_open DATE,
    date_close DATE,
    status_id INTEGER,
    notes TEXT
);

CREATE TABLE materials (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name TEXT,
    cost INTEGER,
    worksheet_id INTEGER,
    notes TEXT
);

CREATE TABLE wsheet2resource (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    worksheet_id TEXT,
    resource_id INTEGER,
    hours INTEGER,
    rate INTEGER,
    notes TEXT
);
