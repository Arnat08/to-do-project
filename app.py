from flask import Flask, request, render_template, session, redirect,url_for
from models import db,Users,Tasks
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)


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
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        print(username,email,password)
        user = Users(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))



@app.route('/task', methods=['GET', 'POST'])
def logout():
    return render_template('art.html')


# Добавил проверку логина и пароля
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('task'))
        else:
            error = 'Invalid username or password'
            return render_template('auth/login.html', error=error)
    return render_template('auth/login.html')




# @app.route('/to-do-page', methods=['GET', 'POST'])
# def to_do_page():
#     return render_template('to-do-page.html')
#
# @app.route('/logout', methods=['GET', 'POST'])
# def logout():
#     return render_template('logout.html')
#

if __name__== '__main__':
    app.run()
    with app.app_context():
        db.create_all()


