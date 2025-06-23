import sqlite3

def execute_query(query, params=(), commit=False):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    if commit:
        conn.commit()
        conn.close()
    else:
        results = cursor.fetchall()
        conn.close()
        return results

# Отримати всі завдання певного користувача
def get_tasks_by_user(user_id):
    return execute_query("SELECT * FROM tasks WHERE user_id = ?", (user_id,))

# Вибрати завдання за певним статусом (наприклад, 'new')
def get_tasks_by_status(status):
    return execute_query("SELECT * FROM tasks WHERE status_id=(SELECT id FROM status WHERE name=?)", (status,))

# Оновити статус конкретного завдання
def update_task_status(task_id, new_status):
    execute_query("UPDATE tasks SET status_id=(SELECT id FROM status WHERE name=?) WHERE id=?", (new_status, task_id), commit=True)

# Отримати список користувачів, які не мають жодного завдання
def get_users_without_tasks():
    return execute_query("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks)")

# Додати нове завдання для конкретного користувача
def add_task(user_id, title, description, status="new"):
    execute_query(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES(?, ?, (SELECT id FROM status WHERE name=?), ?)",
        (title, description, status, user_id), commit=True
    )

# Отримати всі завдання, які ще не завершено (не 'completed')
def get_unfinished_tasks():
    return execute_query("SELECT * FROM tasks WHERE status_id<>(SELECT id FROM status WHERE name='completed')")

# Видалити конкретне завдання
def delete_task(task_id):
    execute_query("DELETE FROM tasks WHERE id=?", (task_id,), commit=True)

# Знайти користувачів з певною електронною поштою (за шаблоном)
def search_users_by_email(pattern):
    return execute_query("SELECT * FROM users WHERE email LIKE ?", (pattern,))

# Оновити ім'я користувача
def update_user_name(user_id, new_name):
    execute_query("UPDATE users SET fullname=? WHERE id=?", (new_name, user_id), commit=True)

# Отримати кількість завдань для кожного статусу
def count_tasks_by_status():
    return execute_query(
        "SELECT s.name AS status, COUNT(t.id) AS task_count FROM status s LEFT JOIN tasks t ON s.id=t.status_id GROUP BY s.name"
    )

# Отримати завдання, призначені користувачам з певною доменною частиною email
def get_tasks_by_email_domain(domain):
    return execute_query("SELECT t.* FROM tasks t JOIN users u ON t.user_id=u.id WHERE u.email LIKE ?", (f'%{domain}',))

# Отримати список завдань, що не мають опису
def get_tasks_without_description():
    return execute_query("SELECT * FROM tasks WHERE description IS NULL OR description=''")

# Вибрати користувачів та їхні завдання, які мають статус 'in progress'
def get_users_tasks_by_status(status="in progress"):
    return execute_query(
        "SELECT u.fullname, t.title, t.description FROM tasks t JOIN users u ON t.user_id=u.id WHERE t.status_id=(SELECT id FROM status WHERE name=?)",
        (status,)
    )

# Отримати користувачів та кількість їхніх завдань
def get_users_and_task_counts():
    return execute_query(
        "SELECT u.fullname, COUNT(t.id) AS task_count FROM users u LEFT JOIN tasks t ON u.id=t.user_id GROUP BY u.id"
    )

# Запити для виконання
if __name__ == "__main__":
    print("Завдання для користувача 1:", get_tasks_by_user(1))
    print("Завдання зі статусом 'new':", get_tasks_by_status("new"))
    update_task_status(2, "in progress")
    print("Користувачі без завдань:", get_users_without_tasks())
    add_task(1, "New Task", "Task description", "new")
    print("Незавершені завдання:", get_unfinished_tasks())
    delete_task(3)
    print("Пошук користувачів (@example.net):", search_users_by_email("%@example.net"))
    update_user_name(1, "Bob Boboi")
    print("Кількість завдань за статусом:", count_tasks_by_status())
    print("Завдання за доменом email (@example.com):", get_tasks_by_email_domain("@example.com"))
    print("Завдання без опису:", get_tasks_without_description())
    print("Завдання користувачів зі статусом 'in progress':", get_users_tasks_by_status("in progress"))
    print("Користувачі та кількість їх завдань:", get_users_and_task_counts())