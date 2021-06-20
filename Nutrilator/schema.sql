DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS macros;
DROP TABLE IF EXISTS users_data;
DROP TABLE IF EXISTS food_logs;

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
    goal TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE food_logs(
    user_id INTEGER,
    date TEXT NOT NULL,
    food_name TEXT NOT NULL,
    food_weight INTEGER NOT NULL,
    food_kcal INTEGER NOT NULL,
    food_carbs INTEGER NOT NULL,
    food_protein INTEGER NOT NULL,
    food_fats INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);