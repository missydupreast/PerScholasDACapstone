/* Create a Jira Sprint for this bonus activity
"304 / 400 Bonus Questions"  
Refer to the MySQL topics list for additional skills learned that you might be able to demonstrate.

### Scenarios for Beginners Learning MySQL:

1. **Exploring the Database Schema**: What things should we look into to explore and learn the database and its various objects.
   - Sample Scenario: List all tables in this database and examine the structure.  what else would we like to know? */

SHOW TABLES; -- this dataset has 3 tables (events, locations, and persons)
DESCRIBE events; -- 4 columns (event_id (PK), person_id, location_id, event_date)
DESCRIBE locations; -- 2 columns (location_id (PK), location_name)
DESCRIBE persons; -- 3 columns (person_id (PK), name, status)
EXPLAIN events; -- this outputs the same as DESCRIBE
SHOW COLUMNS FROM persons; -- gives same info as DESCRIBE

# explore newly added tables:
DESCRIBE evidence; -- 2 columns (evidence_id, description)
DESCRIBE evidence_changes;

/*
2. **Basic Data Querying**:
   - Create some basic single table data queries */

SELECT COUNT(person_id) FROM persons; -- there are 14 persons
SELECT COUNT(location_id) FROM locations; -- there are 4 locations
SELECT * FROM locations; -- locations are (park, street, mall, home)
SELECT * FROM events; -- there are 4 events   

SELECT COUNT(evidence_id) FROM evidence; -- there are 13 pieces of evidence
SELECT * FROM evidence;

   #- Create some complex queries using joins
SELECT p.name, p.status, e.event_date
FROM persons p
LEFT JOIN events e ON p.person_id = e.person_id
WHERE p.status = 'missing' AND e.event_date IS NOT NULL;

SELECT p.name, l.location_name, e.event_date
FROM persons p
LEFT JOIN events e ON p.person_id = e.person_id
LEFT JOIN locations l on e.location_id = l.location_id
WHERE l.location_name IS NOT NULL;

   #- Create some complex queries using sub queries.
SELECT p.name, e.event_id 
FROM persons p
JOIN events e ON p.person_id = e.person_id
WHERE e.location_id = (SELECT location_id FROM locations WHERE location_name = 'mall');

SELECT l.location_name
FROM locations l
JOIN events e ON l.location_id = e.location_id
WHERE e.person_id IN (SELECT person_id FROM persons WHERE status = 'missing');
   
   #- Create some queries with the HAVING clause
SELECT p.name, l.location_name
FROM persons p
LEFT JOIN events e ON p.person_id = e.person_id
LEFT JOIN locations l on e.location_id = l.location_id 
GROUP BY l.location_id
HAVING l.location_id < 4;

SELECT e.event_date, l.location_name
FROM events e
JOIN locations l ON e.location_id = l.location_id
GROUP BY e.event_date, e.event_id
HAVING e.event_id BETWEEN 1 AND 4;
   
   #- Create some queries with sorts and limits and such.
SELECT person_id, name
FROM persons
WHERE status = 'missing'
ORDER BY name;

SELECT p.name, e.event_date, p.status
FROM persons p
JOIN events e ON p.person_id = e.person_id
ORDER BY e.event_date DESC
LIMIT 2;

   #- Create some queries using agregates
SELECT l.location_name, COUNT(p.person_id)
FROM persons p
LEFT JOIN events e ON p.person_id = e.person_id
LEFT JOIN locations l on e.location_id = l.location_id
Where p.status = 'missing'
GROUP BY l.location_name;

SELECT l.location_name, COUNT(l.location_id)
FROM locations l 
JOIN events e ON l.location_id = e.location_id
WHERE YEAR(e.event_date) = '2023';

   #- Create some queries using conditional operators
SELECT p.name, CASE
	WHEN p.status = 'missing' THEN 'Open Case'
    WHEN p.status = 'found' THEN 'Case Closed'
    ELSE NULL
    END AS case_status
FROM persons p
ORDER BY case_status DESC; 

   #- Create some queries using group by clause
SELECT p.status, COUNT(p.status)
FROM persons p 
GROUP BY p.status;

SELECT p.name, e.event_date
FROM persons p 
LEFT JOIN events e ON p.person_id = e.person_id
LEFT JOIN locations l on e.location_id = l.location_id
WHERE l.location_id IS NOT NULL
GROUP BY l.location_id;
   
/*
3. **Inserting Data**:
   - Scenario: Add 5 new records to each table (yea, just make stuff up that matches the existing data. */

INSERT INTO locations VALUES
(5, 'Highway'),
(6, 'Campus'),
(7, 'Field'),
(8, 'Parking Lot'),
(9, 'Club');

SELECT* FROM locations;

INSERT INTO events VALUES
(5,5,5,'2023-05-01'),
(6,6,6,'2023-06-01'),
(7,7,7,'2023-07-01'),
(8,8,8,'2023-08-01'),
(9,9,9,'2023-09-01');  

SELECT* FROM events;

INSERT INTO persons VALUES
(15, 'Jacob Smith', 'missing'),
(16, 'Julie Jacobs', 'found'),
(17, 'Brad Banks', 'missing'),
(18, 'Samantha Reese', 'found'),
(19, 'Carrie summers', 'missing');

SELECT* FROM persons;

/* Scenario: look at the tables.  What other information might we expect to collect?  Create statements to add columns, specifying 
apropriate data types, and relationships if possible. */

ALTER TABLE events
ADD COLUMN event_description VARCHAR(255); 

ALTER TABLE persons
ADD COLUMN hair_color VARCHAR(50),
ADD COLUMN eye_color VARCHAR(50),
ADD COLUMN height VARCHAR(50),
ADD COLUMN weight_lbs INT;

/*
4. **Updating Data**:
   - Scenario: Create some update statements to each table that rely on where clauses (yea, just make stuff up that matches the 
   existing data. */

UPDATE persons
SET eye_color = 'blue'
WHERE person_id = 7;

UPDATE persons
SET hair_color = 'brown'
WHERE person_id = 3;

UPDATE persons
SET eye_color = 'brown', hair_color = 'brown', height = '5''9"', weight_lbs = 128  
WHERE person_id = 4;

UPDATE persons
SET eye_color = 'hazel', hair_color = 'brown', height = '5''10"', weight_lbs = 167
WHERE person_id = 7;

# look at the changes:
SELECT * FROM persons;

/*
3. **Index Management**:
   - Scenario: Analyze the database indexes and add appropriate indexes to optimize queries. */

SHOW INDEXES FROM events; -- has indexes for PK-event_id, person_id, and locations_id

CREATE FULLTEXT INDEX idx_description
ON events(event_description); -- added fulltext index on the event_description column

SHOW INDEXES FROM evidence; -- has 1 PK index on evidence_id
SHOW INDEXES FROM locations; -- has 1 index on PK location_id
SHOW INDEXES FROM persons; -- has 1 index on PK person_id
SHOW INDEXES FROM evidence_changes; -- has indexes for PK cahnge_id and evidence_id

CREATE INDEX idx_status
ON persons(status(50));

# Create a Stored Procedure  and test it

DELIMITER $$
CREATE PROCEDURE GetPersonEventDetails (IN person_id INT)
BEGIN
	SELECT p.person_id, p.name, p.status, e.event_id, e.event_date, e.location_id, l.location_name 
    FROM persons p 
    LEFT JOIN events e ON p.person_id = e.person_id
	JOIN locations l ON e.location_id = l.location_id
	WHERE p.person_id = person_id;
END $$
DELIMITER ;

CALL GetPersonEventDetails(7);
CALL GetPersonEventDetails(9);

# DROP PROCEDURE GetPersonEventDetails; -- use this code to drop the procedure

# Create a Stored Function and test it
# I want to create a stored function to calculate the person's age. First I need to add birth_date data.

ALTER TABLE persons
ADD COLUMN birth_date DATE;

UPDATE persons SET birth_date = '1990-05-15' WHERE person_id = 1;
UPDATE persons SET birth_date = '1985-08-22' WHERE person_id = 2;
UPDATE persons SET birth_date = '2000-02-10' WHERE person_id = 3;
UPDATE persons SET birth_date = '1978-11-30' WHERE person_id = 4;

# Now create the function:

DELIMITER $$
CREATE FUNCTION GetAge(birth_date DATE)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE age INT;
    SET age = FLOOR(DATEDIFF(NOW(), DATE(birth_date))/365);
    RETURN age;
END $$
DELIMITER ;

SELECT name, birth_date, GetAge(birth_date) AS age FROM persons WHERE person_id = 2;

# DROP FUNCTION GetAge; -- to drop the function

# Create a Trigger and test it

DELIMITER $$
CREATE TRIGGER updated_evidence_changes
AFTER UPDATE ON evidence
FOR EACH ROW
BEGIN
INSERT INTO evidence_changes (evidence_id, action, change_date)
VALUES (NEW.evidence_id, 'UPDATE', NOW());
END;
$$
DELIMITER ;

UPDATE evidence
SET description = 'Eyewitness C'
WHERE evidence_id = 12;

SELECT * FROM evidence_changes;

# Create some views */

CREATE VIEW MissingPersonsDetails AS
SELECT p.name, p.status, p.hair_color, p.eye_color, p.height, p.weight_lbs, GetAge(birth_date) AS age, e.event_id, e.event_date, l.location_name
FROM persons p 
LEFT JOIN events e ON p.person_id = e.person_id
JOIN locations l ON e.location_id = l.location_id
WHERE p.status = 'missing';

SELECT * FROM MissingPersonsDetails;

CREATE VIEW VideoEvidence AS
SELECT * FROM evidence WHERE description LIKE 'Video%';
