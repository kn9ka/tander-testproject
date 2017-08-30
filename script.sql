CREATE TABLE IF NOT EXISTS city (
    name TEXT UNIQUE NOT NULL, 
    id_region INTEGER
);

CREATE TABLE IF NOT EXISTS region (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS maindata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    second_name TEXT,
    first_name TEXT,
    patronymic TEXT,
    region INTEGER,
    city INTEGER,
    mobile TEXT,
    email TEXT,
    comment TEXT
);

INSERT OR IGNORE INTO city (name, id_region) VALUES 
    ('Краснодар', 1), 
    ('Кропоткин', 1),
    ('Славянск', 1),
    ('Ростов', 2),
    ('Шахты', 2),
    ('Батайск', 2),
    ('Ставрополь', 3),
    ('Пятигорск', 3),
    ('Кисловодск', 3);
    
INSERT OR IGNORE INTO region (name) VALUES 
    ('Краснодарский край'),
    ('Ростовская область'),
    ('Ставропольский край');