import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

conn = sqlite3.connect("C:/Users/cat-b/PycharmProjects/pythonProject2/base.db")
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Создание таблицы событий
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Event (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        location TEXT NOT NULL,
        description TEXT NOT NULL
    )
''')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM User WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Пользователь уже зарегистрирован. Пожалуйста, войдите."
        else:
            cursor.execute("INSERT INTO User (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return redirect(url_for('create_event'))  # Перенаправление на страницу создания мероприятия

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect('C:/Users/cat-b/PycharmProjects/pythonProject2/base.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM User WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        conn.close()  # закрытие соединения

        if user:
            return redirect(url_for('create_event'))
        else:
            return redirect(url_for('register'))

    return render_template('login.html')


# Функция create_event с изменениями
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    conn = sqlite3.connect('C:/Users/cat-b/PycharmProjects/pythonProject2/base.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        description = request.form['description']

        cursor.execute("INSERT INTO Event (title, date, time, location, description) VALUES (?, ?, ?, ?, ?)",
                       (title, date, time, location, description))
        conn.commit()


        conn.close()
        return redirect(url_for('events_list_page'))


    return render_template('create_event.html')

@app.route('/events_list_page')
def events_list_page():
    conn = sqlite3.connect('C:/Users/cat-b/PycharmProjects/pythonProject2/base.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Event")
    events = cursor.fetchall()

    conn.close()

    return render_template('events_list.html', events=events)

    # Новый маршрут для редактирования мероприятия
@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if request.method == 'POST':
        return f"Мероприятие с ID {event_id} успешно отредактировано!"
    else:
        render_template('edit_event.html', event_id=event_id)


@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    cursor.execute("DELETE FROM Event WHERE id=?", (event_id,))
    conn.commit()
    return f"Мероприятие с ID {event_id} успешно удалено!"


if __name__ == '__main__':
    app.run(debug=True)
    conn.close()
