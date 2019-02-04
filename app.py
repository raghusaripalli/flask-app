from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
app = Flask(__name__)
Articles = Articles()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/articles")
def articles():
    return render_template("articles.html", articles=Articles)


@app.route("/article/<string:aid>/")
def article(aid):
    return render_template("article.html", id=aid)


@app.route("/about")
def about():
    return render_template("about.html")


class RegisterForm(Form):
    name = StringField(u'Name', validators=[validators.input_required(), validators.Length(min=3, max=50)])
    username = StringField(u'Username', validators=[validators.input_required(), validators.Length(min=3, max=25)])
    email = StringField(u'Email', validators=[validators.Email("Wrong Email Format"), validators.Length(min=6, max=50)])
    password = PasswordField(u'Password', validators=[
        validators.DataRequired(),
        validators.equal_to('confirm', message='Passwords do not match'),
        validators.input_required()
    ])
    confirm = PasswordField(u'Confirm Password')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        pass

    return render_template('register.html', form=form)


if __name__ == '__main__':

    # Put debug = False in Production environment
    app.run(debug=True)
