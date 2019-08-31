import sqlite3

conn = sqlite3.connect('static/database.db')
conn.execute('CREATE TABLE users (name TEXT not null, email TEXT primary key not null, password TEXT not null)')
conn.execute('CREATE TABLE expenses (email TEXT, added TEXT, value INT, foreign key(email) references users(email))')
