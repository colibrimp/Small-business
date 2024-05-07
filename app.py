
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Float
from datetime import datetime
from flask_moment import Moment
import smtplib



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
    full_description = db.Column(db.Text, nullable=False)
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


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("localhost", 1025) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


@app.route('/page/<int:index>')
def page(index):
    with app.app_context():
        post_objects = Posts.query.all()
        for post in post_objects:
            if post.id == index:
                requested_post = post
    return render_template('page.html', post=requested_post)


if __name__ == '__main__':
    app.run(debug=True)

