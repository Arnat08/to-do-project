from flask import Flask, request, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.secret_key = '!)@.Y~VqN0+F[;O'
db = SQLAlchemy(app)




class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    tasks = db.relationship('Tasks', lazy=True)

    def init(self, username, email,  password):
        self.username = username
        self.email = email
        self.password = password


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, status, user_id):
        self.title = title
        self.status = status
        self.user_id = user_id


def login_required(route):
    def decorated_route(*args, **kwargs):
        if not session.get('username'):
            return redirect('/login')

        return route(*args, **kwargs)

    return decorated_route


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main.html')     #главная страница


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')


# Добавил проверку @mail на уникальность
        if password == confirm_password:
             existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            return render_template('auth/register.html', error='Электронная почта уже существует') # Можно на английском: Email already exists

        user = Users(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect('/login')


@app.route('/task', methods=['GET', 'POST'])
def logout():
    return render_template('art.html')


# Добавил проверку логина и пароля
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user and user.password == password:
            session['username'] = email
            return redirect('/task') # Добавил адрес to do страницы
        else:
            return render_template('auth/login.html', error='Invalid username or password')

    return render_template('auth/login.html')




# @app.route('/to-do-page', methods=['GET', 'POST'])
# def to_do_page():
#     return render_template('to-do-page.html')
#
# @app.route('/logout', methods=['GET', 'POST'])
# def logout():
#     return render_template('logout.html')
#

if __name__== 'main':
    with app.app_context():
        db.create_all()
    app.run(debug=True)