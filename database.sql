-- database.sql

DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Presence;
DROP TABLE IF EXISTS Item_stolen;
DROP TABLE IF EXISTS Statement;

CREATE TABLE Person (
    person_id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    gender VARCHAR(10),
    hair_color VARCHAR(50),
    eye_color VARCHAR(50),
    skin_color VARCHAR(50),
    clothing VARCHAR(200),
    role VARCHAR(50),
    is_suspect BOOLEAN
);
CREATE TABLE Presence (
    presence_id INTEGER PRIMARY KEY,
    person_id INTEGER,
    arrived_at DATETIME,
    left_at DATETIME,
    was_working BOOLEAN
);
CREATE TABLE Item_stolen (
    item_id INTEGER PRIMARY KEY,
    description VARCHAR(100),
    person_id INTEGER,
    time_of_crime DATETIME
);
CREATE TABLE Statement (
    statement_id INTEGER PRIMARY KEY,
    person_id INTEGER,
    observation_time DATETIME,
    statement_text VARCHAR(500)
);

start transaction;



insert into Product values('A', 1001, 'pc');


commit;

SELECT maker, type, COUNT(*) as count
FROM Product
GROUP BY maker, type
ORDER BY maker, type;

