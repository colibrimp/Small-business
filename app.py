
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Float
from datetime import datetime
from flask_moment import Moment






app = Flask(__name__)

moment = Moment(app)



# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///small_business.db"
# Create the extension
db = SQLAlchemy(model_class=Base)
# initialise the app with the extension
db.init_app(app)



class Posts(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    image_file = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    quote_text = db.Column(db.Text, nullable=True)
    fool_description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)



    def __repr__(self):
        return f'<Posts {self.title}>'




with app.app_context():
    db.create_all()



@app.route('/')
def home():
    with app.app_context():
        current_time = datetime.now().year
        posts = Posts.query.all()
    return render_template('index.html', year=current_time, posts=posts)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/page/')
def page():
    with app.app_context():
        posts = Posts.query.all()
    return render_template('page.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)

