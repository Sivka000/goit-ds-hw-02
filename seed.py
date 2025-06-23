import sqlite3
import random

from faker import Faker
from create_tabl import create_tables # Імпорт коду з create_tabl.py

fake = Faker()
create_tables() # Створення таблиці

# Підключення до бази даних
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
fake = Faker()

# Генерація користувачів
user_ids = [cursor.execute("INSERT INTO users (fullname, email) VALUES (?, ?)", (fullname, email)).lastrowid
            for fullname, email in ((fake.name(), fake.unique.email()) for _ in range(10))]

# Додавання статусів
if not cursor.execute("SELECT 1 FROM status LIMIT 1").fetchone():
    cursor.executemany("INSERT INTO status (name) VALUES (?)", [('new',), ('in progress',), ('completed',)])

# Отримання списку статусів
cursor.execute("SELECT id, name FROM status;")
statuses = cursor.fetchall()
status_ids = [row[0] for row in statuses]

# Генерація завдань
cursor.executemany(
    "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
    [(fake.sentence(nb_words=6), fake.text(max_nb_chars=200), random.choice(status_ids), random.choice(user_ids))
     for _ in range(30)]
)

conn.commit()
conn.close()

print("База даних успішно заповнена!")
