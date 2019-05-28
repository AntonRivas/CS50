CREATE TABLE flights(

id SERIAL PRIMARY KEY,
origin VARCHAR NOT NULL,
destination VARCHAR NOT NULL,
duration INTEGER NOT NULL

);

-- inserting data into the database

INSERT INTO flights (origin, destination, duration) VALUES ('New York', 'Amsterdam', 512);

-- selecting data from the database
SELECT * FROM flights;

SELECT origin, destination FROM flights;

SELECT * FROM flights WHERE id = 3;

-- using the built in average function

SELECT AVG(duration) FROM flights;

-- using the built in count function

SELECT COUNT(*) FROM flights;

-- updating data within the database

UPDATE flights SET duration = 420 WHERE origin = 'New York' AND destination = 'Amsterdam';

-- deleting data

DELETE FROM flights WHERE destination = 'Tokyo';

-- limiting

SELECT * FROM flights LIMIT 2;

-- selecting ordered lists

SELECT * FROM flights ORDER BY duration ASC;

-- grouping data by a parameter

SELECT origin, COUNT(*) FROM flights GROUP BY origin;

-- selecting data from two different spreadsheets and joining them

SELECT origin, destination, name FROM flights JOIN passangers ON passangers.flight_id = flights.id

-- types of JOIN (LEFT JOIN, JOIN and RIGHT JOIN)

-- Note: I havent bothered ACTUALLY making a passangers table

-- Nesting Queries

SELECT * FROM flights WHERE id IN (SELECT flight_id FROM passangers GROUP BY flight_id HAVING COUNT(*) > 1)

-- SQL transactions

BEGIN ;

--Add commands here

COMMIT
