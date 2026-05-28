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
    was_working BOOLEAN,

    FOREIGN KEY (person_id)
        REFERENCES Person(person_id)
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

INSERT INTO Person VALUES
(4, 'Marcus Reed',
 'male',
 'black',
 'brown',
 'lightbrown',
 'striped shirt, tan bakery apron, dark rolled trousers, green beanie, brown work boots',
 'bakery employee',
 FALSE
);

INSERT INTO Person VALUES
(5, 'Elena Bloom',
 'female',
 'greybrown',
 'green',
 'olive',
 'cream blouse, sage-green florist apron, rust midi skirt, brown lace-up boots',
 'florist employee',
 FALSE
);

INSERT INTO Person VALUES
(6, 'Rafael Moreno',
 'male',
 'darkbrown',
 'brown',
 'tan',
 'burgundy overshirt, dark t-shirt, khaki trousers, brown messenger bag, worn sneakers',
 'witness',
 FALSE
);

INSERT INTO Person VALUES
(7, 'Luna Hart',
 'female',
 'strawberryblonde',
 'blue',
 'fair',
 'charcoal beanie, denim vest, cream graphic sweatshirt, black skirt, black tights, platform sneakers',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(8, 'Nia Carter',
 'female',
 'darkbrown',
 'hazel',
 'darkbrown',
 'rust-orange cropped jacket, black graphic crop top, wide blue jeans, black chunky boots',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(9, 'Rowan Vale',
 'nonbinary',
 'silvergrey',
 'greygreen',
 'olive',
 'long plaid overshirt, black top, tan trousers, belt chain, black skate sneakers',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(10, 'Jamal Brooks',
 'male',
 'black',
 'brown',
 'mediumbrown',
 'sage bomber jacket, cream hoodie, black cargo pants, green-white high-top sneakers',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(1, 'Sofia Laurent',
 'female',
 'auburn',
 'green',
 'mediumbrown',
 'navy blazer, cream blouse, charcoal trousers, brown loafers, gold accessories',
 'investigator',
 FALSE
);

INSERT INTO Person VALUES
(2, 'Maya Johnson',
 'female',
 'darkbrown',
 'brown',
 'darkbrown',
 'olive overshirt, brown coffee t-shirt, black cafe apron, patterned brown cargo pants, black high-top sneakers',
 'cafe employee',
 FALSE
);

INSERT INTO Person VALUES
(3, 'Alex Wren',
 'nonbinary',
 'tealblack',
 'darkbrown',
 'fair',
 'charcoal cardigan, mustard scarf, burgundy trousers, round glasses, brown loafers, staff lanyard',
 'bookstore employee',
 FALSE
);

INSERT INTO Person VALUES
(11, 'Clara Finch',
 'female',
 'red',
 'green',
 'fair',
 'teal beanie, oversized teal sweater, white shirt, plaid trousers, messenger bag with pins, chunky cream sneakers',
 'reporter',
 FALSE
);

INSERT INTO Person VALUES
(12, 'Isabella Cruz',
 'female',
 'covered',
 'brown',
 'darkbrown',
 'yellow cropped jacket, teal patterned jumpsuit, brown crossbody bag, gold earrings, colorful bracelets, white sneakers',
 'market employee',
 FALSE
);

INSERT INTO Person VALUES
(13, 'Hiro Tanaka',
 'male',
 'silvergrey',
 'brown',
 'tan',
 'dark blue work coat, cream shirt, blue striped scarf, grey trousers, brown tool bag, brown work boots',
 'watchmaker',
 FALSE
);

INSERT INTO Person VALUES
(14, 'Priya Kapoor',
 'female',
 'blackgrey',
 'brown',
 'mediumbrown',
 'green long coat, mustard tunic, patterned maroon scarf, maroon wide trousers, brown boots, gold jewelry',
 'art dealer',
 FALSE
);

INSERT INTO Person VALUES
(15, 'Rex Voss',
 'male',
 'platinumblonde',
 'brown',
 'fair',
 'black leather jacket, burgundy graphic t-shirt, ripped dark green jeans, chains, fingerless gloves, black combat boots',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(16, 'Amara Rodriguez',
 'female',
 'darkbrown',
 'amberbrown',
 'mediumbrown',
 'navy jewelry-store dress, cream cardigan, navy scarf, name tag, gold earrings, navy flats with gold diamond detail',
 'jewelry employee',
 FALSE
);

INSERT INTO Person VALUES
(17, 'Eleanor Whitmore',
 'female',
 'silvergrey',
 'green',
 'fair',
 'cream blouse, navy vest, navy long skirt, navy scarf, reading glasses, name tag, navy low heels',
 'senior jewelry employee',
 FALSE
);

INSERT INTO Person VALUES
(18, 'Jordan Ellis',
 'nonbinary',
 'auburn',
 'hazel',
 'olive',
 'navy suit, cream turtleneck, name tag, gold necklace, navy loafers',
 'jewelry employee',
 FALSE
);

INSERT INTO Person VALUES
(19, 'James Thompson',
 'male',
 'black',
 'brown',
 'darkbrown',
 'cream shirt, navy vest with gold trim, navy tie, navy trousers, name tag, brown dress shoes',
 'jewelry employee',
 FALSE
);

INSERT INTO Person VALUES
(20, 'Mei Sato',
 'female',
 'darkbrown',
 'brown',
 'fair',
 'navy blazer, cream blouse, navy pencil skirt, navy neck scarf, name tag, black heels',
 'jewelry employee',
 FALSE
);

INSERT INTO Person VALUES
(21, 'Valentina Moretti',
 'female',
 'darkbrown',
 'hazel',
 'mediumbrown',
 'pink trench coat, teal blouse, white wide-leg trousers, gold earrings, bracelets, metallic bronze boots',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(22, 'Arthur Kingsley',
 'male',
 'white',
 'brown',
 'darkbrown',
 'teal blazer, cream turtleneck, grey trousers, grey flat cap, glasses, cane, burgundy dress shoes',
 'collector',
 FALSE
);

INSERT INTO Person VALUES
(23, 'Yumi Nakamura',
 'female',
 'black',
 'brown',
 'fair',
 'coral bomber jacket, white graphic t-shirt, navy pleated skirt, black knee socks, white sneakers, black crossbody bag',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(24, 'Bruno Vargas',
 'male',
 'black',
 'brown',
 'tan',
 'orange utility vest, light blue shirt, olive cargo trousers, black watch, tan work boots',
 'delivery driver',
 FALSE
);

INSERT INTO Person VALUES
(25, 'Margaret Green',
 'female',
 'white',
 'brown',
 'fair',
 'lavender cardigan, yellow blouse, emerald green long skirt, pearl earrings, glasses, burgundy shoes',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(26, 'Scarlett Hayes',
 'female',
 'red',
 'blue',
 'fair',
 'teal blouse, black pencil skirt, black tights, gold earrings, black loafers',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(27, 'Nova Blake',
 'nonbinary',
 'silvergrey',
 'green',
 'mediumbrown',
 'mustard shirt, black turtleneck, black trousers, black boots, watch, necklace',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(28, 'Adrian Wolfe',
 'male',
 'brown',
 'hazel',
 'olive',
 'tan trench coat, black turtleneck, dark trousers, black belt, black loafers',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(29, 'Zara Monroe',
 'female',
 'blonde',
 'brown',
 'darkbrown',
 'burgundy turtleneck, beige trousers, brown belt, gold necklace, brown heeled boots',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(30, 'Daniel Pierce',
 'male',
 'brown',
 'blue',
 'fair',
 'dark green jacket, cream shirt, dark blue jeans, brown belt, brown dress shoes',
 'customer',
 FALSE
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








commit;

SELECT maker, type, COUNT(*) as count
FROM Product
GROUP BY maker, type
ORDER BY maker, type;

