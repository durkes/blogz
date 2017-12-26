from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:demo@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'x737kJcyz&zP3T'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    body = db.Column(db.String(2400))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['static', 'index', 'blog_list', 'login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/blog')
def blog_list():
    return render_template('blog.html', pg_title="Blogz - All Posts")


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    pg_title="Blogz - New Post"

    if request.method == 'GET':
        return render_template('newpost.html', pg_title=pg_title)

    return render_template('newpost.html', pg_title=pg_title)


@app.route('/login', methods=['POST', 'GET'])
def login():
    pg_title="Blogz - Login"

    if request.method == 'GET':
        return render_template('login.html', pg_title=pg_title)

    flash('Error msg test', 'error')
    return render_template('login.html', pg_title=pg_title)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    pg_title="Blogz - Signup"

    if request.method == 'GET':
        return render_template('signup.html', pg_title=pg_title)

    # POST request:
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']

    error = False
    username_error = ""
    password_error = ""
    verify_error = ""

    if len(username) < 3 or len(username) > 20:
        error = True
        username_error = "Must be between 3-20 chars"

    if re.match("^[\w-]*$", username) == None:
        error = True
        username_error = "Only use alphanumeric chars"

    if len(password) < 3 or len(password) > 20:
        error = True
        password_error = "Must be between 3-20 chars"

    if re.match("^[\S-]*$", password) == None:
        error = True
        password_error = "Do not use spaces"

    if verify != password:
        error = True
        verify_error = "Passwords don't match"

    # Input error
    if error:
        return render_template('signup.html', pg_title=pg_title,
            username=username,
            username_error=username_error,
            password_error=password_error,
            verify_error=verify_error)

    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        # success!
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect('/newpost')

    # Username taken
    username_error = "Username already exists"
    return render_template('signup.html', pg_title=pg_title,
        username=username,
        username_error=username_error)


@app.route('/logout')
def logout():
    flash('Logged out')
    del session['username']
    return redirect('/blog')


@app.route('/')
def index():
    return render_template('index.html', pg_title="Blogz - Users")


if __name__ == '__main__':
    app.run()
