USE job_worksheets;

INSERT INTO customers (name, notes) VALUES ("Bob", "Be sure ot check the day before.");
INSERT INTO customers (name, notes) VALUES ("Tim", "Can't backup to save his life");
INSERT INTO customers (name, notes) VALUES ("Steven", "Always a little loose with the hours");
INSERT INTO customers (name, notes) VALUES ("Dale", "Great end dumper");
INSERT INTO customers (name, notes) VALUES ("Susan", "Wno't need any supervision");
INSERT INTO customers (name, notes) VALUES ("Steve", "Pain in the ass");

INSERT INTO jobs (name, customer_id, status_id) VALUES ("digger bobs", 1, 1);
INSERT INTO jobs (name, customer_id, status_id) VALUES ("Killer pit", 3 ,1);
INSERT INTO jobs (name, customer_id, status_id) VALUES ("Doppy Ridge", 2 ,2);
INSERT INTO jobs (name, customer_id, status_id) VALUES ("I5 Paving", 4, 1);
INSERT INTO jobs (name, customer_id, status_id) VALUES ("205 Pot Holes", 4, 1);
INSERT INTO jobs (name, customer_id, status_id) VALUES ("Bobs Back Yard", 1, 1);
INSERT INTO jobs (name, customer_id, status_id) VALUES ("Steves Driveway", 5, 2);

INSERT INTO worksheets (jobs_id, status_id) VALUES ( 1, 2);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 1,1);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 1,2);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 1, 1);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 2,2);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 2,2);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 2,2);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 2,2);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 3,1);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 3,1);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 3,2);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 3,1);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 4,2);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 4,2);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 4,1);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 4,1);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 5,1);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 5,1);
INSERT INTO worksheets (jobs_id, status_id) VALUES ( 6,1);

INSERT INTO materials (name, cost, worksheet_id) VALUES ("boards",23.5,1);
INSERT INTO materials (name, cost, worksheet_id) VALUES ("dirt",67.3,2);
INSERT INTO materials (name, cost, worksheet_id) VALUES ("rock",65,3);
INSERT INTO materials (name, cost, worksheet_id) VALUES ("3/4 minus",23,3);
INSERT INTO materials (name, cost, worksheet_id) VALUES ("sand",654,1);
INSERT INTO materials (name, cost, worksheet_id) VALUES ("air",234,4);
INSERT INTO materials (name, cost, worksheet_id) VALUES ("pipe",23.23,2);

INSERT INTO wsheet2resource (worksheet_id, resource_id, hours) VALUES (2,0,8);
INSERT INTO wsheet2resource (worksheet_id, resource_id, hours) VALUES (3,0,8);
INSERT INTO wsheet2resource (worksheet_id, resource_id, hours) VALUES (4,1,3);
INSERT INTO wsheet2resource (worksheet_id, resource_id, hours) VALUES (1,1,2);
INSERT INTO wsheet2resource (worksheet_id, resource_id, hours) VALUES (1,1,3);
INSERT INTO wsheet2resource (worksheet_id, resource_id, hours) VALUES (3,2,4);
INSERT INTO wsheet2resource (worksheet_id, resource_id, hours) VALUES (5,2,5);
INSERT INTO wsheet2resource (worksheet_id, resource_id, hours) VALUES (2,3,4);
INSERT INTO wsheet2resource (worksheet_id, resource_id, hours) VALUES (2,4,1);
INSERT INTO wsheet2resource (worksheet_id, resource_id, hours) VALUES (4,3,2);
INSERT INTO wsheet2resource (worksheet_id, resource_id, hours) VALUES (2,4,3);