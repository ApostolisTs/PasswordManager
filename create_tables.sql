CREATE TABLE users(
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

CREATE TABLE accounts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_type TEXT NOT NULL,
    username TEXT,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    user TEXT NOT NULL
);
