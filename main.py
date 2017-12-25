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

    def __init__(self, email, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['static', 'index', 'blog_list', 'login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/blog')
def blog_list():
    return render_template('blog.html', title="Blogz - All Posts")


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'GET':
        return render_template('newpost.html', title="Blogz - New Post")

    return render_template('newpost.html', title="Blogz - New Post")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title="Blogz - Login")

    flash('Error msg test', 'error')
    return render_template('login.html', title="Blogz - Login")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', title="Blogz - Signup")

    flash('Error msg test', 'error')
    return render_template('signup.html', title="Blogz - Signup")


@app.route('/logout')
def logout():
    flash('Logged out')
    del session['username']
    return redirect('/blog')


@app.route('/')
def index():
    return render_template('index.html', title="Blogz - Users")


if __name__ == '__main__':
    app.run()
