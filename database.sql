
DROP VIEW IF EXISTS Map_marker_view;
DROP VIEW IF EXISTS Timeline_event_view;
DROP VIEW IF EXISTS Access_log_view;

DROP TABLE IF EXISTS Arrest_guess;
DROP TABLE IF EXISTS Player_suspicion;
DROP TABLE IF EXISTS Evidence;
DROP TABLE IF EXISTS Map_marker;
DROP TABLE IF EXISTS Alibi;
DROP TABLE IF EXISTS Statement;
DROP TABLE IF EXISTS Item_stolen;
DROP TABLE IF EXISTS Presence;
DROP TABLE IF EXISTS Person;

CREATE TABLE Person (
    person_id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    gender VARCHAR(10),
    hair_color VARCHAR(50),
    eye_color VARCHAR(50),
    skin_color VARCHAR(50),
    clothing VARCHAR(200),
    role VARCHAR(50),
    age INTEGER,
    date_of_birth DATE,
    is_suspect BOOLEAN,
    truthfull BOOLEAN
);

CREATE TABLE Alibi (
    person_id INTEGER PRIMARY KEY,
    formatted_alibi VARCHAR(700),

    FOREIGN KEY (person_id)
        REFERENCES Person(person_id)
);

CREATE TABLE Presence (
    presence_id INTEGER PRIMARY KEY,
    person_id INTEGER,
    arrived_at TIMESTAMP,
    left_at TIMESTAMP,
    was_working BOOLEAN,

    FOREIGN KEY (person_id)
        REFERENCES Person(person_id)
);

CREATE TABLE Item_stolen (
    item_id INTEGER PRIMARY KEY,
    description VARCHAR(100),
    person_id INTEGER,
    time_of_crime TIMESTAMP
);

CREATE TABLE Evidence (
    evidence_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    description VARCHAR(300),
    image_filename VARCHAR(100),
    related_person_id INTEGER,

    FOREIGN KEY (related_person_id)
        REFERENCES Person(person_id)
);

CREATE TABLE Map_marker (
    marker_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    x_percent NUMERIC(5,2),
    y_percent NUMERIC(5,2),
    color VARCHAR(20),
    person_id INTEGER,

    FOREIGN KEY (person_id)
        REFERENCES Person(person_id)
);

CREATE TABLE Player_suspicion (
    game_id INTEGER,
    person_id INTEGER,
    is_suspicious BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (game_id, person_id),

    FOREIGN KEY (person_id)
        REFERENCES Person(person_id)
);

CREATE TABLE Arrest_guess (
    game_id INTEGER PRIMARY KEY,
    person_id INTEGER,
    is_correct BOOLEAN,
    guessed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (person_id)
        REFERENCES Person(person_id)
);


CREATE TABLE Statement (
    statement_id INTEGER PRIMARY KEY,
    person_id INTEGER,
    observation_time TIMESTAMP,
    statement_text VARCHAR(500),
    is_truthful BOOLEAN,

    FOREIGN KEY (person_id)
        REFERENCES Person(person_id)
);



CREATE VIEW Access_log_view AS
SELECT
    p.person_id,
    p.name AS person,
    p.role,
    pr.arrived_at,
    pr.left_at,
    pr.was_working
FROM Presence pr
JOIN Person p ON p.person_id = pr.person_id;

CREATE VIEW Timeline_event_view AS
SELECT
    pr.presence_id * 2 - 1 AS event_id,
    p.name,
    pr.arrived_at AS event_time,
    'arrival' AS event_type
FROM Presence pr
JOIN Person p ON p.person_id = pr.person_id
UNION ALL
SELECT
    pr.presence_id * 2 AS event_id,
    p.name,
    pr.left_at AS event_time,
    'departure' AS event_type
FROM Presence pr
JOIN Person p ON p.person_id = pr.person_id
UNION ALL
SELECT
    100000 AS event_id,
    'Robbery' AS name,
    MIN(time_of_crime) AS event_time,
    'event' AS event_type
FROM Item_stolen;

CREATE VIEW Map_marker_view AS
SELECT
    m.marker_id,
    COALESCE(p.name, m.name) AS name,
    m.x_percent,
    m.y_percent,
    COALESCE(m.color, '#cc2200') AS color,
    m.person_id
FROM Map_marker m
LEFT JOIN Person p ON p.person_id = m.person_id;

start transaction;

INSERT INTO Person VALUES
(1, 'Sofia Laurent',
 'female',
 'red',
 'green',
 'mediumbrown',
 'blue blazer, white blouse, grey trousers, brown shoes, gold jewelry',
 'investigator',

 34,
 '1992-02-14',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(2, 'Maya Johnson',
 'female',
 'darkbrown',
 'brown',
 'darkbrown',
 'green shirt, brown t-shirt, black apron, brown pants, black sneakers',
 'cafe employee',

 29,
 '1996-08-03',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(3, 'Alex Wren',
 'nonbinary',
 'black',
 'darkbrown',
 'fair',
 'grey cardigan, yellow scarf, red trousers, glasses, brown shoes, staff lanyard',
 'bookstore employee',

 31,
 '1994-11-19',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(4, 'Marcus Weed',
 'male',
 'black',
 'brown',
 'lightbrown',
 'striped shirt, brown apron, dark trousers, green beanie, brown boots',
 'bakery employee',

 42,
 '1984-04-27',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(5, 'Elena Bloom',
 'female',
 'greybrown',
 'green',
 'olive',
 'white blouse, green apron, red skirt, brown boots',
 'florist employee',

 38,
 '1987-06-09',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(6, 'Rafael Moreno',
 'male',
 'darkbrown',
 'brown',
 'tan',
 'red shirt, black t-shirt, brown pants, brown bag, sneakers',
 'witness',

 35,
 '1991-01-22',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(7, 'Luna Hart',
 'female',
 'blonde',
 'blue',
 'fair',
 'grey beanie, blue vest, white sweater, black skirt, sneakers',
 'customer',

 24,
 '2001-09-16',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(8, 'Nia Carter',
 'female',
 'darkbrown',
 'hazel',
 'darkbrown',
 'orange jacket, black top, blue jeans, black boots',
 'customer',

 27,
 '1999-03-30',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(9, 'Rowan Vale',
 'nonbinary',
 'silvergrey',
 'greygreen',
 'olive',
 'grey shirt, black top, brown pants, black sneakers',
 'customer',

 33,
 '1992-12-05',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(10, 'Jamal Brooks',
 'male',
 'black',
 'brown',
 'mediumbrown',
 'green jacket, white sweater, black pants, green sneakers',
 'customer',

 40,
 '1985-07-11',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(11, 'Clara Finch',
 'female',
 'red',
 'green',
 'fair',
 'blue beanie, green sweater, white shirt, grey pants, bag, sneakers',
 'reporter',

 32,
 '1993-10-25',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(12, 'Isabella Cruz',
 'female',
 'covered',
 'brown',
 'darkbrown',
 'yellow jacket, blue jumpsuit, brown bag, gold earrings, white sneakers',
 'market employee',

 36,
 '1990-05-08',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(13, 'Hiro Tanaka',
 'male',
 'silvergrey',
 'brown',
 'tan',
 'dark blue coat, white shirt, blue scarf, grey trousers, brown bag, brown boots',
 'watchmaker',

 58,
 '1968-01-17',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(14, 'Priya Kapoor',
 'female',
 'blackgrey',
 'brown',
 'mediumbrown',
 'green coat, yellow shirt, red scarf, red pants, brown boots, gold jewelry',
 'art dealer',

 45,
 '1980-09-29',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(15, 'Rex Voss',
 'male',
 'platinumblonde',
 'brown',
 'fair',
 'black leather jacket, red t-shirt, green jeans, chains, gloves, black boots',
 'customer',

 30,
 '1995-06-06',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(16, 'Amara Rodriguez',
 'female',
 'darkbrown',
 'amberbrown',
 'mediumbrown',
 'blue dress, white cardigan, blue scarf, name tag, gold earrings, blue shoes',
 'jewelry employee',

 28,
 '1998-04-13',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(17, 'Eleanor Whitmore',
 'female',
 'silvergrey',
 'green',
 'fair',
 'white blouse, blue vest, blue long skirt, blue scarf, glasses, name tag, blue shoes',
 'senior jewelry employee',

 61,
 '1964-12-02',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(18, 'Jordan Ellis',
 'nonbinary',
 'red',
 'hazel',
 'olive',
 'blue suit, white turtleneck, name tag, gold necklace, blue shoes',
 'jewelry employee',

 26,
 '1999-07-21',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(19, 'James Thompson',
 'male',
 'black',
 'brown',
 'darkbrown',
 'white shirt, blue vest, blue tie, blue trousers, name tag, brown shoes',
 'jewelry employee',

 39,
 '1987-02-18',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(20, 'Mei Sato',
 'female',
 'darkbrown',
 'brown',
 'fair',
 'blue blazer, white blouse, blue skirt, blue scarf, name tag, black shoes',
 'jewelry employee',

 33,
 '1992-10-12',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(21, 'Valentina Moretti',
 'female',
 'darkbrown',
 'hazel',
 'mediumbrown',
 'pink coat, blue blouse, white pants, gold earrings, bracelets, shoes',
 'customer',

 41,
 '1985-03-04',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(22, 'Arthur Kingsley',
 'male',
 'white',
 'brown',
 'darkbrown',
 'blue blazer, white turtleneck, grey trousers, grey cap, glasses, cane, red shoes',
 'collector',

 67,
 '1958-08-26',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(23, 'Yumi Nakamura',
 'female',
 'black',
 'brown',
 'fair',
 'red jacket, white t-shirt, blue skirt, black socks, white sneakers, black bag',
 'customer',

 23,
 '2003-05-15',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(24, 'Bruno Vargas',
 'male',
 'black',
 'brown',
 'tan',
 'orange vest, blue shirt, green pants, black watch, brown boots',
 'delivery driver',

 37,
 '1988-11-01',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(25, 'Margaret Green',
 'female',
 'white',
 'brown',
 'fair',
 'purple cardigan, yellow blouse, green long skirt, pearl earrings, glasses, red shoes',
 'customer',

 72,
 '1954-04-20',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(26, 'Scarlett Hayes',
 'female',
 'red',
 'blue',
 'fair',
 'blue blouse, black skirt, black tights, gold earrings, black shoes',
 'customer',

 25,
 '2001-01-07',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(27, 'Nova Blake',
 'nonbinary',
 'silvergrey',
 'green',
 'mediumbrown',
 'yellow shirt, black turtleneck, black trousers, black boots, watch, necklace',
 'customer',

 29,
 '1996-06-24',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(28, 'Adrian Wolfe',
 'male',
 'brown',
 'hazel',
 'olive',
 'brown coat, black turtleneck, dark trousers, black belt, black shoes',
 'customer',

 44,
 '1981-09-10',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(29, 'Zara Monroe',
 'female',
 'blonde',
 'brown',
 'darkbrown',
 'red turtleneck, brown trousers, brown belt, gold necklace, brown boots',
 'customer',

 31,
 '1994-12-28',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(30, 'Daniel Pierce',
 'male',
 'brown',
 'blue',
 'fair',
 'green jacket, white shirt, blue jeans, brown belt, brown shoes',
 'customer',

 46,
 '1980-02-05',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(31, 'Isabella Marino',
 'female',
 'black',
 'brown',
 'light / tan',
 'turquoise blouse, white trousers, gold earrings, gold bracelets, sunglasses on head, gold heels',
 'luxury fashion consultant',

 31,
 '1995-08-09',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(32, 'Darius King',
 'male',
 'black',
 'brown / hidden behind sunglasses',
 'dark',
 'purple blazer, black shirt, white trousers, gold chain, sunglasses, black shoes',
 'club owner',

 39,
 '1987-02-27',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(33, 'Luca Valenti',
 'male',
 'black',
 'brown / hidden behind sunglasses',
 'light / tan',
 'floral open shirt, white trousers, gold necklaces, sunglasses, light green loafers',
 'tourist / private collector',

 29,
 '1997-06-14',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(34, 'Marco Valenti',
 'male',
 'black',
 'brown / hidden behind sunglasses',
 'light / tan',
 'white suit, turquoise shirt, gold chain, sunglasses, brown shoes',
 'wealthy jewelry investor',

 34,
 '1992-04-18',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(35, 'Naomi Brooks',
 'female',
 'dark brown / black',
 'brown',
 'dark',
 'pink blazer, black dress, gold jewelry, white heels',
 'event promoter',

 28,
 '1998-11-03',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(36, 'Mateo Cruz',
 'male',
 'black',
 'brown',
 'light / tan',
 'red plaid shirt, white t-shirt, dark jeans, black boots, silver chain',
 'local mechanic',

 27,
 '1999-10-04',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(37, 'Raymond Brooks',
 'male',
 'black / hidden under cap',
 'brown / hidden behind sunglasses',
 'dark',
 'yellow polo shirt, dark jeans, tan boots, black cap, sunglasses, gold chain',
 'music producer',

 42,
 '1984-03-21',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(38, 'Mei Tanaka',
 'female',
 'black',
 'brown',
 'light / tan',
 'burgundy bomber jacket, black crop top, black wide trousers, red and white sneakers, gold jewelry',
 'dancer',

 25,
 '2001-07-18',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(39, 'Diego Alvarez',
 'male',
 'black',
 'brown',
 'light / tan',
 'green short-sleeved shirt, white tank top, beige trousers, white sneakers, gold necklace, green bandana',
 'lowrider club member',

 30,
 '1996-01-29',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(40, 'Aaliyah Carter',
 'female',
 'black',
 'brown',
 'dark',
 'green varsity jacket, black crop top, khaki cargo pants, green and white sneakers, gold jewelry',
 'streetwear influencer',

 24,
 '2002-05-12',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(41, 'Silas Voss',
 'male',
 'black with silver / white streaks',
 'brown',
 'light / pale',
 'long black coat, black graphic shirt, black trousers, black gloves, black boots, chains and necklaces',
 'nightclub dj',

 26,
 '2000-02-11',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(42, 'Violet Reyes',
 'female',
 'black with purple highlights',
 'brown',
 'light / tan',
 'red plaid jacket, black skull shirt, ripped black jeans, black boots, chains, bracelets and earrings',
 'tattoo apprentice',

 24,
 '2002-06-25',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(43, 'Phoenix Vale',
 'male',
 'bright orange',
 'brown',
 'light / pale',
 'black leather jacket, striped mesh shirt, red plaid trousers, black platform boots, chains and piercings',
 'alternative fashion designer',

 28,
 '1998-12-03',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(44, 'Jax Morgan',
 'male',
 'green',
 'brown',
 'dark',
 'black sleeveless denim vest with patches, black hoodie, black ripped jeans, black combat boots, chains and studded wristbands',
 'street artist',

 27,
 '1999-04-08',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(45, 'Raven Cross',
 'female',
 'blonde / light blond',
 'brown',
 'light / tan',
 'black leather jacket with pins, dark graphic shirt, red plaid skirt, ripped fishnet tights, black combat boots, chains and chokers',
 'punk musician',

 23,
 '2003-09-17',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(46, 'Malik Cross',
 'male',
 'black',
 'brown',
 'dark',
 'long black coat, black turtleneck, black vest, black trousers, black boots, silver necklaces and rings',
 'private security consultant',

 32,
 '1994-01-19',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(47, 'Elara Voss',
 'female',
 'black with dark blue tones',
 'brown',
 'light / pale',
 'black gothic dress, black gloves, black lace details, black boots, choker and dark jewelry',
 'costume designer',

 29,
 '1997-10-06',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(48, 'Lucien Blackwell',
 'male',
 'black with silver / grey streaks',
 'grey / brown',
 'very light / pale',
 'long black coat, black vest, black shirt, black trousers, black gloves, black boots, chains and necklaces',
 'antique dealer',

 34,
 '1992-04-23',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(49, 'Selene Moreau',
 'female',
 'black',
 'brown',
 'medium / tan',
 'black leather jacket, black corset-style top, black lace skirt, black trousers, black platform boots, chains and gothic jewelry',
 'gothic jewelry collector',

 30,
 '1996-08-14',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(50, 'Cassandra Night',
 'female',
 'black',
 'brown',
 'light / pale',
 'long black velvet coat, black lace dress, black corset, black platform boots, layered necklaces and rings',
 'occult shop owner',

 31,
 '1995-12-02',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(51, 'Adrian Moretti',
 'male',
 'dark brown / black',
 'brown',
 'medium / tan',
 'dark navy coat, dark vest, striped shirt, dark trousers, brown dress shoes, gold necklace and bracelets',
 'art dealer',

 36,
 '1990-05-27',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(52, 'Serena Vale',
 'female',
 'black',
 'brown',
 'medium / tan',
 'black leather jacket, dark hoodie, red scarf, black ripped jeans, black combat boots, crossbody bag',
 'freelance photographer',

 27,
 '1999-09-02',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(53, 'Ash Mercer',
 'male',
 'bright orange',
 'brown',
 'light / pale',
 'black leather jacket with pins, black graphic shirt, dark plaid trousers, black combat boots, fingerless gloves, chains and earrings',
 'punk guitarist',

 25,
 '2001-03-18',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(54, 'Marcus Reed',
 'male',
 'black',
 'brown',
 'dark',
 'green varsity jacket, black hoodie, olive cargo pants, tan work boots, gold necklace and chain',
 'delivery driver',

 33,
 '1993-11-11',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(55, 'Kenji Sato',
 'male',
 'black',
 'brown',
 'light / tan',
 'long black coat, black turtleneck, black shirt, black trousers, black combat boots, silver chain and rings',
 'fashion buyer',

 30,
 '1996-07-24',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(56, 'Nova Reyes',
 'female',
 'black',
 'brown',
 'medium / tan',
 'burgundy bomber jacket, black mesh crop top, black cargo pants, black combat boots, fingerless gloves, gold necklaces and chains',
 'street dancer',

 26,
 '2000-04-16',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(57, 'Ellie Harper',
 'female',
 'brown',
 'brown',
 'light',
 'green raincoat, brown hoodie, layered shirt, ripped patched jeans, brown combat boots, backpack and guitar case',
 'street musician',

 22,
 '2004-09-08',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(58, 'Oliver Wren',
 'male',
 'white / platinum blond',
 'light brown / grey',
 'very light / pale',
 'worn brown overcoat, brown sweater vest, beige shirt, green scarf, loose olive trousers, brown shoes, round glasses, tote bag and old book',
 'history student',

 24,
 '2002-01-30',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(59, 'Hector Morales',
 'male',
 'dark brown / black',
 'brown',
 'medium / tan',
 'blue denim jacket, dark hoodie, worn cargo pants, brown work boots, dark cap, backpack and rolled sleeping mat',
 'street drifter',

 48,
 '1978-06-19',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(60, 'Hana Mori',
 'female',
 'white / grey',
 'brown',
 'light / tan',
 'long worn raincoat, brown cardigan, long dark skirt, blue scarf, dark shoes, shoulder bag, thermos and newspaper',
 'retired seamstress',

 74,
 '1952-03-12',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(61, 'Lila Bennett',
 'female',
 'brown',
 'brown',
 'light / tan',
 'green raincoat, brown hoodie, patched jeans, brown boots, backpack and guitar case',
 'street musician',

 23,
 '2003-06-09',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(62, 'Ezra Whitlock',
 'male',
 'white / platinum blond',
 'light brown / grey',
 'very light / pale',
 'worn brown coat, brown sweater vest, beige shirt, green scarf, loose olive trousers, brown shoes, round glasses, tote bag and old book',
 'history student',

 24,
 '2002-11-14',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(63, 'Tomas Rivera',
 'male',
 'dark brown / black',
 'brown',
 'medium / tan',
 'blue denim jacket, dark hoodie, worn cargo pants, brown work boots, dark cap, backpack and rolled sleeping mat',
 'street drifter',

 49,
 '1977-08-04',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(64, 'Mira Santos',
 'female',
 'black',
 'brown',
 'medium / tan',
 'burgundy bomber jacket, black mesh top, black cargo pants, black combat boots, fingerless gloves, gold chains and earrings',
 'street performer',

 28,
 '1998-02-21',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(65, 'Milo Bennett',
 'male',
 'black',
 'brown',
 'light / tan',
 'orange vest, white shirt, plaid shorts, long socks, checkered shoes, camera and magnifying glass',
 'school student',

 9,
 '2017-05-14',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(66, 'Zuri Brooks',
 'female',
 'dark brown / black',
 'brown',
 'dark',
 'blue denim overalls, turquoise hoodie, colorful socks, colorful sneakers, purple backpack, braided hair',
 'school student',

 10,
 '2016-08-03',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(67, 'Theo Carter',
 'male',
 'curly dark brown / black',
 'brown',
 'dark',
 'yellow raincoat, red and white striped shirt, green shorts, colorful socks, red sneakers, round glasses',
 'school student',

 8,
 '2018-01-21',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(68, 'Nia Alvarez',
 'female',
 'dark brown / black',
 'brown',
 'light / tan',
 'yellow patterned dress, burgundy cardigan, dark leggings, brown boots, brown shoulder bag, short curly hair',
 'school student',

 11,
 '2015-10-09',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(69, 'Finn Whitlock',
 'male',
 'bright orange / red',
 'brown',
 'light',
 'green sweater vest, cream shirt, beige trousers, suspenders, green high-top shoes, flashlight and marbles',
 'school student',

 9,
 '2017-03-27',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(70, 'Amara Brooks',
 'female',
 'dark brown / black',
 'brown',
 'dark',
 'navy bomber jacket, pink shirt, dark skirt, black tights, high-top sneakers, headphones and notebook',
 'school student',

 11,
 '2015-04-22',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(71, 'Clara Whitlock',
 'female',
 'white / platinum blond',
 'light brown / grey',
 'very light / pale',
 'lavender coat, striped shirt, cream trousers, brown boots, round glasses, small shoulder bag',
 'school student',

 10,
 '2016-02-11',
 FALSE,
 TRUE
);

INSERT INTO Person VALUES
(72, 'Mateo Rivera',
 'male',
 'black',
 'brown',
 'light / tan',
 'yellow hoodie, navy trousers, blue and white sneakers, crossbody bag',
 'school student',

 9,
 '2017-07-03',
 FALSE,
 TRUE
);

INSERT INTO Presence VALUES
(1, 1, '2026-05-12 13:05:00', '2026-05-12 18:00:00', TRUE);

INSERT INTO Presence VALUES
(2, 2, '2026-05-12 07:30:00', '2026-05-12 15:30:00', TRUE);

INSERT INTO Presence VALUES
(3, 3, '2026-05-12 09:15:00', '2026-05-12 17:45:00', TRUE);

INSERT INTO Presence VALUES
(4, 4, '2026-05-12 06:00:00', '2026-05-12 14:00:00', TRUE);

INSERT INTO Presence VALUES
(5, 5, '2026-05-12 08:00:00', '2026-05-12 16:00:00', TRUE);

INSERT INTO Presence VALUES
(6, 6, '2026-05-12 11:45:00', '2026-05-12 12:20:00', FALSE);

INSERT INTO Presence VALUES
(7, 7, '2026-05-12 12:05:00', '2026-05-12 12:50:00', FALSE);

INSERT INTO Presence VALUES
(8, 8, '2026-05-12 12:10:00', '2026-05-12 12:45:00', FALSE);

INSERT INTO Presence VALUES
(9, 9, '2026-05-12 12:00:00', '2026-05-12 12:40:00', FALSE);

INSERT INTO Presence VALUES
(10, 10, '2026-05-12 12:15:00', '2026-05-12 13:05:00', FALSE);

INSERT INTO Presence VALUES
(11, 11, '2026-05-12 13:20:00', '2026-05-12 16:30:00', TRUE);

INSERT INTO Presence VALUES
(12, 12, '2026-05-12 08:30:00', '2026-05-12 17:00:00', TRUE);

INSERT INTO Presence VALUES
(13, 13, '2026-05-12 09:00:00', '2026-05-12 16:30:00', TRUE);

INSERT INTO Presence VALUES
(14, 14, '2026-05-12 11:30:00', '2026-05-12 12:55:00', FALSE);

INSERT INTO Presence VALUES
(15, 15, '2026-05-12 12:20:00', '2026-05-12 12:38:00', FALSE);

INSERT INTO Presence VALUES
(16, 16, '2026-05-12 09:00:00', '2026-05-12 17:30:00', TRUE);

INSERT INTO Presence VALUES
(17, 17, '2026-05-12 08:45:00', '2026-05-12 17:15:00', TRUE);

INSERT INTO Presence VALUES
(18, 18, '2026-05-12 09:30:00', '2026-05-12 18:00:00', TRUE);

INSERT INTO Presence VALUES
(19, 19, '2026-05-12 09:00:00', '2026-05-12 17:00:00', TRUE);

INSERT INTO Presence VALUES
(20, 20, '2026-05-12 10:00:00', '2026-05-12 18:30:00', TRUE);

INSERT INTO Presence VALUES
(21, 21, '2026-05-12 12:05:00', '2026-05-12 12:48:00', FALSE);

INSERT INTO Presence VALUES
(22, 22, '2026-05-12 11:55:00', '2026-05-12 13:10:00', FALSE);

INSERT INTO Presence VALUES
(23, 23, '2026-05-12 12:25:00', '2026-05-12 12:42:00', FALSE);

INSERT INTO Presence VALUES
(24, 24, '2026-05-12 12:18:00', '2026-05-12 12:34:00', TRUE);

INSERT INTO Presence VALUES
(25, 25, '2026-05-12 11:40:00', '2026-05-12 12:15:00', FALSE);

INSERT INTO Presence VALUES
(26, 26, '2026-05-12 12:00:00', '2026-05-12 12:33:00', FALSE);

INSERT INTO Presence VALUES
(27, 27, '2026-05-12 12:12:00', '2026-05-12 12:52:00', FALSE);

INSERT INTO Presence VALUES
(28, 28, '2026-05-12 11:50:00', '2026-05-12 12:45:00', FALSE);

INSERT INTO Presence VALUES
(29, 29, '2026-05-12 12:08:00', '2026-05-12 12:58:00', FALSE);

INSERT INTO Presence VALUES
(30, 30, '2026-05-12 11:35:00', '2026-05-12 12:25:00', FALSE);

INSERT INTO Presence VALUES
(31, 31, '2026-05-12 13:10:00', '2026-05-12 13:55:00', FALSE);

INSERT INTO Presence VALUES
(32, 32, '2026-05-12 13:30:00', '2026-05-12 14:10:00', FALSE);

INSERT INTO Presence VALUES
(33, 33, '2026-05-12 13:05:00', '2026-05-12 13:40:00', FALSE);

INSERT INTO Presence VALUES
(34, 34, '2026-05-12 13:20:00', '2026-05-12 14:05:00', FALSE);

INSERT INTO Presence VALUES
(35, 35, '2026-05-12 13:25:00', '2026-05-12 14:00:00', FALSE);

INSERT INTO Presence VALUES
(36, 36, '2026-05-12 13:15:00', '2026-05-12 14:00:00', FALSE);

INSERT INTO Presence VALUES
(37, 37, '2026-05-12 13:05:00', '2026-05-12 13:50:00', FALSE);

INSERT INTO Presence VALUES
(38, 38, '2026-05-12 13:25:00', '2026-05-12 14:15:00', FALSE);

INSERT INTO Presence VALUES
(39, 39, '2026-05-12 12:50:00', '2026-05-12 13:45:00', FALSE);

INSERT INTO Presence VALUES
(40, 40, '2026-05-12 12:55:00', '2026-05-12 13:35:00', FALSE);

INSERT INTO Presence VALUES
(41, 41, '2026-05-12 13:20:00', '2026-05-12 14:05:00', FALSE);

INSERT INTO Presence VALUES
(42, 42, '2026-05-12 13:15:00', '2026-05-12 14:10:00', FALSE);

INSERT INTO Presence VALUES
(43, 43, '2026-05-12 12:55:00', '2026-05-12 13:40:00', FALSE);

INSERT INTO Presence VALUES
(44, 44, '2026-05-12 13:25:00', '2026-05-12 14:15:00', FALSE);

INSERT INTO Presence VALUES
(45, 45, '2026-05-12 13:05:00', '2026-05-12 13:50:00', FALSE);

INSERT INTO Presence VALUES
(46, 46, '2026-05-12 13:10:00', '2026-05-12 14:00:00', FALSE);

INSERT INTO Presence VALUES
(47, 47, '2026-05-12 13:25:00', '2026-05-12 14:15:00', FALSE);

INSERT INTO Presence VALUES
(48, 48, '2026-05-12 12:55:00', '2026-05-12 13:45:00', FALSE);

INSERT INTO Presence VALUES
(49, 49, '2026-05-12 13:20:00', '2026-05-12 14:05:00', FALSE);

INSERT INTO Presence VALUES
(50, 50, '2026-05-12 13:05:00', '2026-05-12 13:55:00', FALSE);

INSERT INTO Presence VALUES
(51, 51, '2026-05-12 13:15:00', '2026-05-12 14:05:00', FALSE);

INSERT INTO Presence VALUES
(52, 52, '2026-05-12 13:05:00', '2026-05-12 13:55:00', FALSE);

INSERT INTO Presence VALUES
(53, 53, '2026-05-12 12:55:00', '2026-05-12 13:45:00', FALSE);

INSERT INTO Presence VALUES
(54, 54, '2026-05-12 13:20:00', '2026-05-12 14:10:00', FALSE);

INSERT INTO Presence VALUES
(55, 55, '2026-05-12 13:00:00', '2026-05-12 13:50:00', FALSE);

INSERT INTO Presence VALUES
(56, 56, '2026-05-12 13:10:00', '2026-05-12 14:00:00', FALSE);

INSERT INTO Presence VALUES
(57, 57, '2026-05-12 12:50:00', '2026-05-12 13:40:00', FALSE);

INSERT INTO Presence VALUES
(58, 58, '2026-05-12 13:05:00', '2026-05-12 13:55:00', FALSE);

INSERT INTO Presence VALUES
(59, 59, '2026-05-12 13:20:00', '2026-05-12 14:10:00', FALSE);

INSERT INTO Presence VALUES
(60, 60, '2026-05-12 12:45:00', '2026-05-12 13:35:00', FALSE);

INSERT INTO Presence VALUES
(61, 61, '2026-05-12 12:55:00', '2026-05-12 13:45:00', FALSE);

INSERT INTO Presence VALUES
(62, 62, '2026-05-12 13:05:00', '2026-05-12 13:55:00', FALSE);

INSERT INTO Presence VALUES
(63, 63, '2026-05-12 13:20:00', '2026-05-12 14:10:00', FALSE);

INSERT INTO Presence VALUES
(64, 64, '2026-05-12 13:10:00', '2026-05-12 14:00:00', FALSE);

INSERT INTO Presence VALUES
(65, 65, '2026-05-12 13:10:00', '2026-05-12 13:50:00', FALSE);

INSERT INTO Presence VALUES
(66, 66, '2026-05-12 13:05:00', '2026-05-12 13:45:00', FALSE);

INSERT INTO Presence VALUES
(67, 67, '2026-05-12 13:15:00', '2026-05-12 13:55:00', FALSE);

INSERT INTO Presence VALUES
(68, 68, '2026-05-12 13:00:00', '2026-05-12 13:50:00', FALSE);

INSERT INTO Presence VALUES
(69, 69, '2026-05-12 12:55:00', '2026-05-12 13:40:00', FALSE);

INSERT INTO Presence VALUES
(70, 70, '2026-05-12 13:05:00', '2026-05-12 13:45:00', FALSE);

INSERT INTO Presence VALUES
(71, 71, '2026-05-12 13:10:00', '2026-05-12 13:55:00', FALSE);

INSERT INTO Presence VALUES
(72, 72, '2026-05-12 13:15:00', '2026-05-12 13:55:00', FALSE);


INSERT INTO Item_stolen VALUES
(1, 'Aurora diamond necklace', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(2, 'Emerald pendant with gold chain', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(3, 'Sapphire earrings in velvet case', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(4, 'Pearl bracelet with silver clasp', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(5, 'Ruby ring from VIP display', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(6, 'Gold pocket watch with initials', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(7, 'Antique brooch shaped like a rose', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(8, 'Diamond tennis bracelet', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(9, 'Rare opal ring in black box', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(10, 'Golden charm bracelet with sun symbol', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(11, 'Blue topaz necklace from front display', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(12, 'Engraved wedding band set', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(13, 'Luxury wristwatch with leather strap', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(14, 'Small velvet pouch of loose diamonds', NULL, '2026-05-12 12:30:00');

INSERT INTO Item_stolen VALUES
(15, 'Nordlys collection centerpiece necklace', NULL, '2026-05-12 12:30:00');

INSERT INTO Evidence VALUES
(1, 'Evidence 1', 'Shovel found at the crime scene', 'Evidens 1.png', NULL);

INSERT INTO Map_marker VALUES
(1, 'Maison Aurora Jewelry', 50.50, 47.00, '#cc2200', NULL);






INSERT INTO Statement VALUES
(1, 1, '2026-05-12 13:20:00',
 'I arrived after the alarm, but one witness kept mentioning someone with {{culprit_hair_color}} hair. That detail may matter.',
 TRUE
);

INSERT INTO Statement VALUES
(2, 2, '2026-05-12 12:25:00',
 'During my coffee shift, I saw someone with {{culprit_skin_color}} skin moving quickly near the jewelry store entrance.',
 TRUE
);

INSERT INTO Statement VALUES
(3, 3, '2026-05-12 12:10:00',
 'A customer in the bookshop asked strange questions about expensive necklaces. I remember something about {{culprit_clothing}}.',
  TRUE
);

INSERT INTO Statement VALUES
(4, 4, '2026-05-12 12:05:00',
 'I was carrying bread outside the bakery when I noticed someone with {{culprit_hair_color}} hair looking toward the jewelry window.',
 TRUE
);

INSERT INTO Statement VALUES
(5, 5, '2026-05-12 12:18:00',
 'I was arranging flowers outside when someone with {{culprit_eye_color}} eyes passed by twice. They seemed nervous.',
 TRUE
);

INSERT INTO Statement VALUES
(6, 6, '2026-05-12 12:20:00',
 'I saw someone leave the area around {{crime_time}}. I mostly remember the outfit: {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(7, 7, '2026-05-12 12:32:00',
 'I was near the display window when someone with {{culprit_hair_color}} hair brushed past me.',
 TRUE
);

INSERT INTO Statement VALUES
(8, 8, '2026-05-12 12:35:00',
 'I heard footsteps right before the alarm. When I turned around, I noticed someone wearing {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(9, 9, '2026-05-12 12:28:00',
 'Someone with {{culprit_skin_color}} skin was standing unusually close to the side entrance. I thought it was odd.',
 TRUE
);

INSERT INTO Statement VALUES
(10, 10, '2026-05-12 12:40:00',
 'I remember seeing a {{culprit_gender}} person near the store around the time of the theft.',
 TRUE
);

INSERT INTO Statement VALUES
(11, 11, '2026-05-12 13:45:00',
 'For my report, I wrote down one detail from a witness: {{culprit_hair_color}} hair. It came up more than once.',
 TRUE
);

INSERT INTO Statement VALUES
(12, 12, '2026-05-12 12:22:00',
 'From my market stall, I saw someone with {{culprit_eye_color}} eyes staring at the police car before walking away.',
 TRUE
);

INSERT INTO Statement VALUES
(13, 13, '2026-05-12 12:15:00',
 'I repair watches, so I notice small details. The person I saw had {{culprit_hair_color}} hair and moved with purpose.',
 TRUE
);

INSERT INTO Statement VALUES
(14, 14, '2026-05-12 12:27:00',
 'I was looking at the displays when someone wearing {{culprit_clothing}} came very close to the VIP case.',
 TRUE
);

INSERT INTO Statement VALUES
(15, 15, '2026-05-12 12:31:00',
 'I did not see the face clearly, but I remember {{culprit_hair_color}} hair near the alley entrance.',
 TRUE
);

INSERT INTO Statement VALUES
(16, 16, '2026-05-12 12:29:00',
 'I was helping a customer when I noticed someone with {{culprit_skin_color}} skin near the counter where {{stolen_item}} was displayed.',
 TRUE
);

INSERT INTO Statement VALUES
(17, 17, '2026-05-12 12:26:00',
 'I have worked here for years. The person near the display did not behave like a normal customer. I noticed {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(18, 18, '2026-05-12 12:33:00',
 'Someone passed behind me just before the alarm. I remember seeing {{culprit_hair_color}} hair reflected in the glass case.',
 TRUE
);

INSERT INTO Statement VALUES
(19, 19, '2026-05-12 12:24:00',
 'I greeted someone around {{crime_time}}, but they avoided eye contact. Their eyes looked {{culprit_eye_color}}.',
 TRUE
);

INSERT INTO Statement VALUES
(20, 20, '2026-05-12 12:36:00',
 'I was checking the front display when I noticed a person with {{culprit_skin_color}} skin leaving in a hurry.',
 TRUE
);

INSERT INTO Statement VALUES
(21, 21, '2026-05-12 12:34:00',
 'I remember someone stylish near the entrance. The clearest thing was the clothing: {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(22, 22, '2026-05-12 12:38:00',
 'Collectors notice details. I saw a {{culprit_gender}} person near the necklace case shortly before the alarm.',
 TRUE
);

INSERT INTO Statement VALUES
(23, 23, '2026-05-12 12:30:00',
 'I was only there briefly, but I saw someone with {{culprit_hair_color}} hair near the door.',
 TRUE
);

INSERT INTO Statement VALUES
(24, 24, '2026-05-12 12:21:00',
 'I had a delivery nearby. Someone with {{culprit_skin_color}} skin crossed in front of me carrying themselves like they were in a rush.',
 TRUE
);

INSERT INTO Statement VALUES
(25, 25, '2026-05-12 12:12:00',
 'I saw someone before I left. I remember thinking their {{culprit_hair_color}} hair stood out.',
 TRUE
);

INSERT INTO Statement VALUES
(26, 26, '2026-05-12 12:29:00',
 'I noticed a person near the side of the room. The outfit looked like {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(27, 27, '2026-05-12 12:37:00',
 'I wrote down what I saw: {{culprit_eye_color}} eyes, quick movements, and a glance toward the display case.',
 TRUE
);

INSERT INTO Statement VALUES
(28, 28, '2026-05-12 12:23:00',
 'Someone passed me near the entrance. I cannot swear to the face, but the person had {{culprit_hair_color}} hair.',
 TRUE
);

INSERT INTO Statement VALUES
(29, 29, '2026-05-12 12:41:00',
 'I saw someone leave after the commotion. The detail I remember best is {{culprit_skin_color}} skin and {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(30, 30, '2026-05-12 12:19:00',
 'Before the alarm, I noticed someone with {{culprit_eye_color}} eyes looking closely at {{stolen_item}}.',
 TRUE
);

INSERT INTO Statement VALUES
(31, 31, '2026-05-12 13:38:00',
 'I heard someone arguing near the display cases. Shortly after, I noticed a person with {{culprit_hair_color}} hair moving away from the store entrance.',
 TRUE
);

INSERT INTO Statement VALUES
(32, 32, '2026-05-12 13:50:00',
 'I saw someone near the back entrance carrying something under one arm. What stood out to me was the person''s {{culprit_skin_color}} skin.',
 TRUE
);

INSERT INTO Statement VALUES
(33, 33, '2026-05-12 13:32:00',
 'I noticed someone acting nervous near the window display. I remember the person had {{culprit_eye_color}} eyes.',
 TRUE
);

INSERT INTO Statement VALUES
(34, 34, '2026-05-12 13:45:00',
 'I saw someone leaving quickly from the side street. I mainly noticed that the person was wearing {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(35, 35, '2026-05-12 13:48:00',
 'Just after the alarm started, I saw someone hurry toward a car outside the store. I only got a clear look at {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(36, 36, '2026-05-12 13:41:00',
 'I noticed someone near the entrance right before people started reacting. I remember the person had {{culprit_hair_color}} hair.',
 TRUE
);

INSERT INTO Statement VALUES
(37, 37, '2026-05-12 13:36:00',
 'I saw someone step away from the display area in a hurry. What stood out to me was the person''s {{culprit_skin_color}} skin.',
 TRUE
);

INSERT INTO Statement VALUES
(38, 38, '2026-05-12 13:52:00',
 'I passed someone who looked nervous near the window display. I remember the person had {{culprit_eye_color}} eyes.',
 TRUE
);

INSERT INTO Statement VALUES
(39, 39, '2026-05-12 13:30:00',
 'I saw someone leave the area near the side of the store. I only clearly noticed {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(40, 40, '2026-05-12 13:22:00',
 'I saw someone moving quickly past the jewelry store. The thing I noticed most was {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(41, 41, '2026-05-12 13:47:00',
 'I noticed someone moving away from the store window after the commotion started. I mostly remember {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(42, 42, '2026-05-12 13:51:00',
 'I passed someone near the display window who seemed nervous. What stood out to me was the person''s {{culprit_eye_color}} eyes.',
 TRUE
);

INSERT INTO Statement VALUES
(43, 43, '2026-05-12 13:29:00',
 'I saw someone hurry down the stairs near the back of the store. I remember the person had {{culprit_skin_color}} skin.',
 TRUE
);

INSERT INTO Statement VALUES
(44, 44, '2026-05-12 13:56:00',
 'I saw someone leave the side of the store quickly. I only got a good look at {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(45, 45, '2026-05-12 13:33:00',
 'I saw someone cut through the alley beside the jewelry store. The only thing I clearly noticed was {{culprit_hair_color}} hair.',
 TRUE
);

INSERT INTO Statement VALUES
(46, 46, '2026-05-12 13:42:00',
 'I saw someone standing close to the jewelry display before leaving quickly. What I noticed most was the person''s {{culprit_skin_color}} skin.',
 TRUE
);

INSERT INTO Statement VALUES
(47, 47, '2026-05-12 13:54:00',
 'I noticed someone moving away from the shop entrance after the alarm. I mostly remember {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(48, 48, '2026-05-12 13:31:00',
 'I saw someone hurry past the side of the store. The clearest thing I noticed was {{culprit_hair_color}} hair.',
 TRUE
);

INSERT INTO Statement VALUES
(49, 49, '2026-05-12 13:49:00',
 'I briefly saw someone turn their head near the window display. I remember the person had {{culprit_eye_color}} eyes.',
 TRUE
);

INSERT INTO Statement VALUES
(50, 50, '2026-05-12 13:37:00',
 'I saw someone leave the alley beside the jewelry store. I only got a clear look at {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(51, 51, '2026-05-12 13:46:00',
 'I saw someone standing close to the jewelry window before leaving the area. I mainly noticed {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(52, 52, '2026-05-12 13:34:00',
 'I saw someone moving quickly near the balcony above the jewelry district. The only thing I clearly noticed was {{culprit_hair_color}} hair.',
 TRUE
);

INSERT INTO Statement VALUES
(53, 53, '2026-05-12 13:28:00',
 'I noticed someone hurry away from the back stairs. What stood out to me was the person''s {{culprit_eye_color}} eyes.',
 TRUE
);

INSERT INTO Statement VALUES
(54, 54, '2026-05-12 13:52:00',
 'I saw someone move away from the side of the store after the commotion. I remember the person had {{culprit_skin_color}} skin.',
 TRUE
);

INSERT INTO Statement VALUES
(55, 55, '2026-05-12 13:39:00',
 'I saw someone leave the alley beside the jewelry store. I only got a clear look at {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(56, 56, '2026-05-12 13:41:00',
 'I saw someone move quickly past the jewelry window. The only thing I clearly noticed was {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(57, 57, '2026-05-12 13:26:00',
 'I noticed someone hurry away from the side of the store. I remember the person had {{culprit_hair_color}} hair.',
 TRUE
);

INSERT INTO Statement VALUES
(58, 58, '2026-05-12 13:37:00',
 'I saw someone glance back near the display cases. What stood out to me was the person''s {{culprit_eye_color}} eyes.',
 TRUE
);

INSERT INTO Statement VALUES
(59, 59, '2026-05-12 13:52:00',
 'I saw someone standing near the shop entrance before moving away. I remember the person had {{culprit_skin_color}} skin.',
 TRUE
);

INSERT INTO Statement VALUES
(60, 60, '2026-05-12 13:24:00',
 'I noticed someone leave the area beside the jewelry store. I only got a clear look at {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(61, 61, '2026-05-12 13:29:00',
 'I noticed someone hurry away from the side of the store. I remember the person had {{culprit_hair_color}} hair.',
 TRUE
);

INSERT INTO Statement VALUES
(62, 62, '2026-05-12 13:36:00',
 'I saw someone glance back near the display cases. What stood out to me was the person''s {{culprit_eye_color}} eyes.',
 TRUE
);

INSERT INTO Statement VALUES
(63, 63, '2026-05-12 13:52:00',
 'I saw someone standing near the shop entrance before moving away. I remember the person had {{culprit_skin_color}} skin.',
 TRUE
);

INSERT INTO Statement VALUES
(64, 64, '2026-05-12 13:42:00',
 'I saw someone move quickly past the jewelry display. The only thing I clearly noticed was {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(65, 65, '2026-05-12 13:32:00',
 'I was looking around with my magnifying glass when I saw someone pass by quickly. I remember the person had {{culprit_hair_color}} hair.',
 TRUE
);

INSERT INTO Statement VALUES
(66, 66, '2026-05-12 13:29:00',
 'I was holding the map when someone rushed past the display cases. I mostly noticed {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(67, 67, '2026-05-12 13:36:00',
 'I was writing in my notebook when I saw someone near the case board. I remember the person had {{culprit_eye_color}} eyes.',
 TRUE
);

INSERT INTO Statement VALUES
(68, 68, '2026-05-12 13:34:00',
 'I was sketching the necklace display when someone moved away from the door. I noticed the person had {{culprit_skin_color}} skin.',
 TRUE
);

INSERT INTO Statement VALUES
(69, 69, '2026-05-12 13:25:00',
 'I was checking the storage room with my flashlight when I saw someone go by. The clearest thing I noticed was {{culprit_hair_color}} hair.',
 TRUE
);

INSERT INTO Statement VALUES
(70, 70, '2026-05-12 13:31:00',
 'I saw someone hurry past the jewelry window. I only really noticed {{culprit_clothing}}.',
 TRUE
);

INSERT INTO Statement VALUES
(71, 71, '2026-05-12 13:35:00',
 'I was looking through my magnifying glass when someone walked away from the jewelry case. I remember the person had {{culprit_eye_color}} eyes.',
 TRUE
);

INSERT INTO Statement VALUES
(72, 72, '2026-05-12 13:34:00',
 'I saw someone run past with something in their hand. I remember the person had {{culprit_skin_color}} skin.',
 TRUE
);

INSERT INTO Alibi (person_id, formatted_alibi) VALUES (1, 'Investigated the case on-site after the alarm. Statement: I arrived after the alarm, but one witness kept mentioning someone with {{culprit_hair_color}} hair. That detail may matter.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (2, 'Worked their coffee shift in the cafe during the incident. Statement: During my coffee shift, I saw someone with {{culprit_skin_color}} skin moving quickly near the jewelry store entrance.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (3, 'Was at work in the bookstore helping customers. Statement: A customer in the bookshop asked strange questions about expensive necklaces. I remember something about {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (4, 'Was standing outside the bakery carrying out freshly baked bread. Statement: I was carrying bread outside the bakery when I noticed someone with {{culprit_hair_color}} hair looking toward the jewelry window.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (5, 'Stayed outside the flower shop arranging plants. Statement: I was arranging flowers outside when someone with {{culprit_eye_color}} eyes passed by twice. They seemed nervous.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (6, 'Was present in the area as an outside witness. Statement: I saw someone leave the area around {{crime_time}}. I mostly remember the outfit: {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (7, 'Walked around the mall as a customer and stood near the display window. Statement: I was near the display window when someone with {{culprit_hair_color}} hair brushed past me.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (8, 'Looked at items as a customer and heard quick footsteps. Statement: I heard footsteps right before the alarm. When I turned around, I noticed someone wearing {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (9, 'Was in the building as a customer close to the side entrance. Statement: Someone with {{culprit_skin_color}} skin was standing unusually close to the side entrance. I thought it was odd.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (10, 'Spent time near the shops in the mall. Statement: I remember seeing a {{culprit_gender}} person near the store around the time of the theft.');

INSERT INTO Alibi (person_id, formatted_alibi) VALUES (11, 'Arrived quickly at the scene to cover the case for their report. Statement: For my report, I wrote down one detail from a witness: {{culprit_hair_color}} hair. It came up more than once.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (12, 'Attended their usual market stall in the square outside. Statement: From my market stall, I saw someone with {{culprit_eye_color}} eyes staring at the police car before walking away.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (13, 'Performed watch repairs inside their workshop. Statement: I repair watches, so I notice small details. The person I saw had {{culprit_hair_color}} hair and moved with purpose.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (14, 'Walked around the mall on business to appraise items. Statement: I was looking at the displays when someone wearing {{culprit_clothing}} came very close to the VIP case.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (15, 'Took a walk in the area and passed the entrance to the alley. Statement: I did not see the face clearly, but I remember {{culprit_hair_color}} hair near the alley entrance.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (16, 'Was at work in the jewelry store helping out at the counter. Statement: I was helping a customer when I noticed someone with {{culprit_skin_color}} skin near the counter where {{stolen_item}} was displayed.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (17, 'Monitored the most expensive display cases in the jewelry store. Statement: I have worked here for years. The person near the display did not behave like a normal customer. I noticed {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (18, 'Stood ready by the glass cases in the jewelry store during their shift. Statement: Someone passed behind me just before the alarm. I remember seeing {{culprit_hair_color}} hair reflected in the glass case.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (19, 'Welcomed visitors at the entrance of the jewelry store. Statement: I greeted someone around {{crime_time}}, but they avoided eye contact. Their eyes looked {{culprit_eye_color}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (20, 'Stayed in the front section of the jewelry store to check the display. Statement: I was checking the front display when I noticed a person with {{culprit_skin_color}} skin leaving in a hurry.');

INSERT INTO Alibi (person_id, formatted_alibi) VALUES (21, 'Was shopping and stood close to the entrance area. Statement: I remember someone stylish near the entrance. The clearest thing was the clothing: {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (22, 'Examined the selection of rare necklaces close to the display case. Statement: Collectors notice details. I saw a {{culprit_gender}} person near the necklace case shortly before the alarm.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (23, 'Was briefly inside the store as a customer to browse the selection. Statement: I was only there briefly, but I saw someone with {{culprit_hair_color}} hair near the door.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (24, 'Was logging or dropping off a delivery nearby. Statement: I had a delivery nearby. Someone with {{culprit_skin_color}} skin crossed in front of me carrying themselves like they were in a rush.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (25, 'Stayed in the store briefly as a customer before moving on. Statement: I saw someone before I left. I remember thinking their {{culprit_hair_color}} hair stood out.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (26, 'Looked at the displays on the other side of the room. Statement: I noticed a person near the side of the room. The outfit looked like {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (27, 'Was in the room as a customer and observed the behavior around the display case. Statement: I wrote down what I saw: {{culprit_eye_color}} eyes, quick movements, and a glance toward the display case.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (28, 'Entered the store and passed the doorway during the theft. Statement: Someone passed me near the entrance. I cannot swear to the face, but the person had {{culprit_hair_color}} hair.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (29, 'Observed the commotion and the exit after the alarm went off. Statement: I saw someone leave after the commotion. The detail I remember best is {{culprit_skin_color}} skin and {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (30, 'Stood looking at the exhibited items in the shop. Statement: Before the alarm, I noticed someone with {{culprit_eye_color}} eyes looking closely at {{stolen_item}}.');

INSERT INTO Alibi (person_id, formatted_alibi) VALUES (31, 'Isabella says she was browsing the front display and then stepped outside to take a phone call. Statement: I heard someone arguing near the display cases. Shortly after, I noticed a person with {{culprit_hair_color}} hair moving away from the store entrance.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (32, 'Darius claims he was outside by his car speaking with a driver and never entered the VIP section of the store. Statement: I saw someone near the back entrance carrying something under one arm. What stood out to me was the person''s {{culprit_skin_color}} skin.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (33, 'Luca says he only stopped outside the store to look at the window display and left before anything suspicious happened. Statement: I noticed someone acting nervous near the window display. I remember the person had {{culprit_eye_color}} eyes.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (34, 'Marco claims he was waiting outside near his car while his business partner looked at jewelry inside the store. Statement: I saw someone leaving quickly from the side street. I mainly noticed that the person was wearing {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (35, 'Naomi claims she was outside taking promotional photos for a nearby event and did not enter the jewelry store. Statement: Just after the alarm started, I saw someone hurry toward a car outside the store. I only got a clear look at {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (36, 'Mateo says he was waiting outside for a friend and was looking toward the street when the theft happened. Statement: I noticed someone near the entrance right before people started reacting. I remember the person had {{culprit_hair_color}} hair.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (37, 'Raymond claims he was outside the shop checking a message on his phone and did not enter the store. Statement: I saw someone step away from the display area in a hurry. What stood out to me was the person''s {{culprit_skin_color}} skin.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (38, 'Mei says she was walking through the jewelry district on her way to meet a friend and only stopped briefly near the store. Statement: I passed someone who looked nervous near the window display. I remember the person had {{culprit_eye_color}} eyes.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (39, 'Diego claims he was standing by his car outside the jewelry store and talking with another person when the theft happened. Statement: I saw someone leave the area near the side of the store. I only clearly noticed {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (40, 'Aaliyah claims she was taking pictures outside the store for her social media and never went inside. Statement: I saw someone moving quickly past the jewelry store. The thing I noticed most was {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (41, 'Silas says he was checking the jewelry display from outside while waiting for a rideshare. Statement: I noticed someone moving away from the store window after the commotion started. I mostly remember {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (42, 'Violet claims she was walking through the alley on her way to meet a friend and did not enter the jewelry store. Statement: I passed someone near the display window who seemed nervous. What stood out to me was the person''s {{culprit_eye_color}} eyes.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (43, 'Phoenix says he was taking reference photos of the alley and store lights for a clothing design project. Statement: I saw someone hurry down the stairs near the back of the store. I remember the person had {{culprit_skin_color}} skin.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (44, 'Jax claims he was outside looking at the jewelry displays and then moved into the alley to avoid the crowd. Statement: I saw someone leave the side of the store quickly. I only got a good look at {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (45, 'Raven claims she was waiting in the alley for a bandmate and only stopped near the jewelry store because it had started raining. Statement: I saw someone cut through the alley beside the jewelry store. The only thing I clearly noticed was {{culprit_hair_color}} hair.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (46, 'Malik claims he was walking through the alley after a meeting nearby and only stopped to look at the jewelry window. Statement: I saw someone standing close to the jewelry display before leaving quickly. What I noticed most was the person''s {{culprit_skin_color}} skin.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (47, 'Elara says she was passing through the alley on her way to a fashion event and did not enter the jewelry store. Statement: I noticed someone moving away from the shop entrance after the alarm. I mostly remember {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (48, 'Lucien claims he was examining the old architecture in the alley and never went inside the store. Statement: I saw someone hurry past the side of the store. The clearest thing I noticed was {{culprit_hair_color}} hair.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (49, 'Selene says she was browsing the outside display because she collects antique jewelry designs. Statement: I briefly saw someone turn their head near the window display. I remember the person had {{culprit_eye_color}} eyes.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (50, 'Cassandra claims she was walking home from a nearby shop and only paused because she heard people shouting near the jewelry store. Statement: I saw someone leave the alley beside the jewelry store. I only got a clear look at {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (51, 'Adrian claims he was waiting outside the jewelry store for a private client and did not enter the shop. Statement: I saw someone standing close to the jewelry window before leaving the area. I mainly noticed {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (52, 'Serena says she was taking skyline photos from the balcony and only looked down toward the store after hearing shouting. Statement: I saw someone moving quickly near the balcony above the jewelry district. The only thing I clearly noticed was {{culprit_hair_color}} hair.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (53, 'Ash claims he was waiting near the stairs for a friend and never went inside the jewelry store. Statement: I noticed someone hurry away from the back stairs. What stood out to me was the person''s {{culprit_eye_color}} eyes.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (54, 'Marcus claims he was standing outside waiting for a delivery pickup and did not know anything had happened until people started gathering. Statement: I saw someone move away from the side of the store after the commotion. I remember the person had {{culprit_skin_color}} skin.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (55, 'Kenji says he was looking at the jewelry displays from outside while waiting for a taxi. Statement: I saw someone leave the alley beside the jewelry store. I only got a clear look at {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (56, 'Nova claims she was waiting in the alley for a friend and only stopped near the jewelry store because of the rain. Statement: I saw someone move quickly past the jewelry window. The only thing I clearly noticed was {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (57, 'Ellie says she was walking through the alley with her guitar case and did not enter the jewelry store. Statement: I noticed someone hurry away from the side of the store. I remember the person had {{culprit_hair_color}} hair.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (58, 'Oliver claims he was looking for an old bookshop nearby and only paused near the jewelry store to check his notes. Statement: I saw someone glance back near the display cases. What stood out to me was the person''s {{culprit_eye_color}} eyes.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (59, 'Hector says he was walking through the alley to find shelter from the rain and was drinking from his cup when the commotion started. Statement: I saw someone standing near the shop entrance before moving away. I remember the person had {{culprit_skin_color}} skin.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (60, 'Hana claims she was reading the newspaper outside the shop and waiting for the rain to slow down before walking home. Statement: I noticed someone leave the area beside the jewelry store. I only got a clear look at {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (61, 'Lila says she was walking through the alley with her guitar case and did not enter the jewelry store. Statement: I noticed someone hurry away from the side of the store. I remember the person had {{culprit_hair_color}} hair.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (62, 'Ezra claims he was looking for an old bookshop nearby and only paused near the jewelry store to check his notes. Statement: I saw someone glance back near the display cases. What stood out to me was the person''s {{culprit_eye_color}} eyes.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (63, 'Tomas says he was walking through the alley to find shelter from the rain and was holding his radio when the commotion started. Statement: I saw someone standing near the shop entrance before moving away. I remember the person had {{culprit_skin_color}} skin.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (64, 'Mira claims she was waiting in the alley for a friend and only looked toward the jewelry store when she heard people shouting. Statement: I saw someone move quickly past the jewelry display. The only thing I clearly noticed was {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (65, 'Milo says he was playing detective near the alley and taking pictures with his camera when the adults started shouting. Statement: I was looking around with my magnifying glass when I saw someone pass by quickly. I remember the person had {{culprit_hair_color}} hair.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (66, 'Zuri says she was trying to follow a map through the jewelry district and stayed close to the front display. Statement: I was holding the map when someone rushed past the display cases. I mostly noticed {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (67, 'Theo says he was writing clues in his notebook and looking at the map board when the commotion started. Statement: I was writing in my notebook when I saw someone near the case board. I remember the person had {{culprit_eye_color}} eyes.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (68, 'Nia says she was drawing jewelry designs in her notebook and stayed near the desk inside the investigation room. Statement: I was sketching the necklace display when someone moved away from the door. I noticed the person had {{culprit_skin_color}} skin.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (69, 'Finn says he was exploring the storage room and counting the colored marbles in his pocket when he heard footsteps outside. Statement: I was checking the storage room with my flashlight when I saw someone go by. The clearest thing I noticed was {{culprit_hair_color}} hair.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (70, 'Amara says she was waiting outside the jewelry store with her notebook while her parents looked at the window display. Statement: I saw someone hurry past the jewelry window. I only really noticed {{culprit_clothing}}.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (71, 'Clara says she was looking around the shop with her magnifying glass while her parents asked about antique jewelry. Statement: I was looking through my magnifying glass when someone walked away from the jewelry case. I remember the person had {{culprit_eye_color}} eyes.');
INSERT INTO Alibi (person_id, formatted_alibi) VALUES (72, 'Mateo says he was in the back office area with his parents and was holding the clue bag when the adults started talking. Statement: I saw someone run past with something in their hand. I remember the person had {{culprit_skin_color}} skin.');

commit;

