from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:demo@localhost:8889/blogz'
# app.config['SQLALCHEMY_ECHO'] = True
# db = SQLAlchemy(app)
# app.secret_key = 'y737kGcys&zP3T'


# class Blog(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(240))
#     body = db.Column(db.String(2400))
#
#     def __init__(self, title, body):
#         self.title = title
#         self.body = body


@app.route('/blog', methods=['GET'])
def blog():
    return render_template('blog.html', title="Blogz")


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    return render_template('newpost.html', title="Blogz")


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html', title="Blogz")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('signup.html', title="Blogz")


@app.route('/')
def index():
    return render_template('index.html', title="Blogz")


if __name__ == '__main__':
    app.run()
