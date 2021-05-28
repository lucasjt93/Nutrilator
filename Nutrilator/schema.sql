DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE macros(
    user_id INTEGER,
    tdee INTEGER NOT NULL,
    protein INTEGER NOT NULL,
    carbo INTEGER NOT NULL,
    fat INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE users_data(
    user_id INTEGER,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    weight INTEGER NOT NULL,
    height INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);