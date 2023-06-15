from functools import wraps
from flask import Flask, request, render_template, session, redirect, url_for
from models import db, Users, Tasks
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)


def login_required(route):
    @wraps(route)
    def decorated_route(*args, **kwargs):
        if not session.get('username'):
            return redirect('/login')

        return route(*args, **kwargs)

    return decorated_route


def login_not_required(route):
    @wraps(route)
    def decorated_route(*args, **kwargs):
        if session.get('username'):
            return redirect(url_for('task'))

        return route(*args, **kwargs)

    return decorated_route


@app.route('/', methods=['GET'])
def main_page():
    if session.get('username'):
        return redirect(url_for('task'))

    return render_template('main.html')  # главная страница


@app.route('/register', methods=['GET', 'POST'])
@login_not_required
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        print(username, email, password)
        user = Users(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('login'))  # Перенаправляем на страницу входа
    return render_template('auth/register.html')  # Исправленный путь к шаблону


@app.route('/login', methods=['GET', 'POST'])
@login_not_required
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('task'))
        else:
            error = 'Invalid username or password'
            return render_template('auth/login.html', error=error)


@app.route('/task', methods=['GET'])
@login_required
def task():
    return render_template('auth/to-do-page.html')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
