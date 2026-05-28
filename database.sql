-- database.sql

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
    is_suspect BOOLEAN
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


CREATE TABLE Statement (
    statement_id INTEGER PRIMARY KEY,
    person_id INTEGER,
    observation_time TIMESTAMP,
    statement_text VARCHAR(500),
    is_truthful BOOLEAN,

    FOREIGN KEY (person_id)
        REFERENCES Person(person_id)
-- Her betyder person_id: personen som siger statementet, ikke den skyldige.
);



start transaction;

INSERT INTO Person VALUES
(1, 'Sofia Laurent',
 'female',
 'red',
 'green',
 'mediumbrown',
 'blue blazer, white blouse, grey trousers, brown shoes, gold jewelry',
 'investigator',
 FALSE
);

INSERT INTO Person VALUES
(2, 'Maya Johnson',
 'female',
 'darkbrown',
 'brown',
 'darkbrown',
 'green shirt, brown t-shirt, black apron, brown pants, black sneakers',
 'cafe employee',
 FALSE
);

INSERT INTO Person VALUES
(3, 'Alex Wren',
 'nonbinary',
 'black',
 'darkbrown',
 'fair',
 'grey cardigan, yellow scarf, red trousers, glasses, brown shoes, staff lanyard',
 'bookstore employee',
 FALSE
);

INSERT INTO Person VALUES
(4, 'Marcus Reed',
 'male',
 'black',
 'brown',
 'lightbrown',
 'striped shirt, brown apron, dark trousers, green beanie, brown boots',
 'bakery employee',
 FALSE
);

INSERT INTO Person VALUES
(5, 'Elena Bloom',
 'female',
 'greybrown',
 'green',
 'olive',
 'white blouse, green apron, red skirt, brown boots',
 'florist employee',
 FALSE
);

INSERT INTO Person VALUES
(6, 'Rafael Moreno',
 'male',
 'darkbrown',
 'brown',
 'tan',
 'red shirt, black t-shirt, brown pants, brown bag, sneakers',
 'witness',
 FALSE
);

INSERT INTO Person VALUES
(7, 'Luna Hart',
 'female',
 'blonde',
 'blue',
 'fair',
 'grey beanie, blue vest, white sweater, black skirt, sneakers',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(8, 'Nia Carter',
 'female',
 'darkbrown',
 'hazel',
 'darkbrown',
 'orange jacket, black top, blue jeans, black boots',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(9, 'Rowan Vale',
 'nonbinary',
 'silvergrey',
 'greygreen',
 'olive',
 'grey shirt, black top, brown pants, black sneakers',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(10, 'Jamal Brooks',
 'male',
 'black',
 'brown',
 'mediumbrown',
 'green jacket, white sweater, black pants, green sneakers',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(11, 'Clara Finch',
 'female',
 'red',
 'green',
 'fair',
 'blue beanie, green sweater, white shirt, grey pants, bag, sneakers',
 'reporter',
 FALSE
);

INSERT INTO Person VALUES
(12, 'Isabella Cruz',
 'female',
 'covered',
 'brown',
 'darkbrown',
 'yellow jacket, blue jumpsuit, brown bag, gold earrings, white sneakers',
 'market employee',
 FALSE
);

INSERT INTO Person VALUES
(13, 'Hiro Tanaka',
 'male',
 'silvergrey',
 'brown',
 'tan',
 'dark blue coat, white shirt, blue scarf, grey trousers, brown bag, brown boots',
 'watchmaker',
 FALSE
);

INSERT INTO Person VALUES
(14, 'Priya Kapoor',
 'female',
 'blackgrey',
 'brown',
 'mediumbrown',
 'green coat, yellow shirt, red scarf, red pants, brown boots, gold jewelry',
 'art dealer',
 FALSE
);

INSERT INTO Person VALUES
(15, 'Rex Voss',
 'male',
 'platinumblonde',
 'brown',
 'fair',
 'black leather jacket, red t-shirt, green jeans, chains, gloves, black boots',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(16, 'Amara Rodriguez',
 'female',
 'darkbrown',
 'amberbrown',
 'mediumbrown',
 'blue dress, white cardigan, blue scarf, name tag, gold earrings, blue shoes',
 'jewelry employee',
 FALSE
);

INSERT INTO Person VALUES
(17, 'Eleanor Whitmore',
 'female',
 'silvergrey',
 'green',
 'fair',
 'white blouse, blue vest, blue long skirt, blue scarf, glasses, name tag, blue shoes',
 'senior jewelry employee',
 FALSE
);

INSERT INTO Person VALUES
(18, 'Jordan Ellis',
 'nonbinary',
 'red',
 'hazel',
 'olive',
 'blue suit, white turtleneck, name tag, gold necklace, blue shoes',
 'jewelry employee',
 FALSE
);

INSERT INTO Person VALUES
(19, 'James Thompson',
 'male',
 'black',
 'brown',
 'darkbrown',
 'white shirt, blue vest, blue tie, blue trousers, name tag, brown shoes',
 'jewelry employee',
 FALSE
);

INSERT INTO Person VALUES
(20, 'Mei Sato',
 'female',
 'darkbrown',
 'brown',
 'fair',
 'blue blazer, white blouse, blue skirt, blue scarf, name tag, black shoes',
 'jewelry employee',
 FALSE
);

INSERT INTO Person VALUES
(21, 'Valentina Moretti',
 'female',
 'darkbrown',
 'hazel',
 'mediumbrown',
 'pink coat, blue blouse, white pants, gold earrings, bracelets, shoes',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(22, 'Arthur Kingsley',
 'male',
 'white',
 'brown',
 'darkbrown',
 'blue blazer, white turtleneck, grey trousers, grey cap, glasses, cane, red shoes',
 'collector',
 FALSE
);

INSERT INTO Person VALUES
(23, 'Yumi Nakamura',
 'female',
 'black',
 'brown',
 'fair',
 'red jacket, white t-shirt, blue skirt, black socks, white sneakers, black bag',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(24, 'Bruno Vargas',
 'male',
 'black',
 'brown',
 'tan',
 'orange vest, blue shirt, green pants, black watch, brown boots',
 'delivery driver',
 FALSE
);

INSERT INTO Person VALUES
(25, 'Margaret Green',
 'female',
 'white',
 'brown',
 'fair',
 'purple cardigan, yellow blouse, green long skirt, pearl earrings, glasses, red shoes',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(26, 'Scarlett Hayes',
 'female',
 'red',
 'blue',
 'fair',
 'blue blouse, black skirt, black tights, gold earrings, black shoes',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(27, 'Nova Blake',
 'nonbinary',
 'silvergrey',
 'green',
 'mediumbrown',
 'yellow shirt, black turtleneck, black trousers, black boots, watch, necklace',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(28, 'Adrian Wolfe',
 'male',
 'brown',
 'hazel',
 'olive',
 'brown coat, black turtleneck, dark trousers, black belt, black shoes',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(29, 'Zara Monroe',
 'female',
 'blonde',
 'brown',
 'darkbrown',
 'red turtleneck, brown trousers, brown belt, gold necklace, brown boots',
 'customer',
 FALSE
);

INSERT INTO Person VALUES
(30, 'Daniel Pierce',
 'male',
 'brown',
 'blue',
 'fair',
 'green jacket, white shirt, blue jeans, brown belt, brown shoes',
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

commit;



