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

    def __init__(self, username, email,  password):
        self.username = username
        self.email = email
        self.password = password


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


def login_required(route):
    def decorated_route(*args, **kwargs):
        if not session.get('username'):
            return redirect('/login')

        return route(*args, **kwargs)

    return decorated_route


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        if password == confirm_password:
            user = Users(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()

            return redirect('/login')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)