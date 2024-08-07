from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# Конфигурация базы данных
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'qwerty123'
app.config['MYSQL_DB'] = 'my_website'

# Инициализация MySQL
mysql = MySQL(app)

# Секретный ключ для сессий
app.secret_key = 'your_secret_key'

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']

        # Проверка существования пользователя
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Пользователь с таким именем уже существует!'
        else:
            # Вставка пользователя в базу данных
            cursor.execute("INSERT INTO users (username, password, name) VALUES (%s, %s, %s)", (username, password, name))
            mysql.connection.commit()
            msg = 'Вы успешно зарегистрированы!'
    return render_template('index.html', msg=msg)

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверка учетных данных
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        account = cursor.fetchone()
        if account:
            # Создание сессии (изменяем доступ к элементу кортежа)
            session['loggedin'] = True
            session['id'] = account[0]  # Доступ к первому элементу кортежа
            session['username'] = account[1]  # Доступ к второму элементу кортежа
            session['name'] = account[3]  # Доступ к четвертому элементу кортежа
            return redirect(url_for('dashboard'))
        else:
            msg = 'Неверные учетные данные!'
    return render_template('index.html', msg=msg)

# Личный кабинет
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        # Получение заметки из базы данных
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT note FROM notes WHERE user_id = %s", (session['id'],))
        note = cursor.fetchone()
        if note:
            note = note[0]
        else:
            note = ''
        return render_template('dashboard.html', name=session['name'], note=note)
    return redirect(url_for('login'))

# Сохранение заметки
@app.route('/save_note', methods=['POST'])
def save_note():
    if 'loggedin' in session:
        note = request.form['note']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM notes WHERE user_id = %s", (session['id'],))
        exists = cursor.fetchone()
        if exists:
            # Обновление существующей заметки
            cursor.execute("UPDATE notes SET note = %s WHERE user_id = %s", (note, session['id']))
        else:
            # Создание новой заметки
            cursor.execute("INSERT INTO notes (user_id, note) VALUES (%s, %s)", (session['id'], note))
        mysql.connection.commit()
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Выход
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('name', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

