from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
app = Flask(__name__)
Articles = Articles()

# MYSql Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Init MySQL
mysql = MySQL(app)


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
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create Cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT into users(name, email, username, password) values (%s,%s,%s,%s)", (
            name, email, username, password
        ))
        # commit to db
        mysql.connection.commit()
        # close the connection
        cur.close()
        # Flash message
        flash('You are now registered and can login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create Cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("select * from users where username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # PASSED
                session['logged_in'] = True
                session['username'] = username
                flash("You are now logged in !!", 'success')
                cur.close()
                return redirect(url_for('dashboard'))
            else:
                error = 'Wrong Password'
                cur.close()
                return render_template("login.html", error=error)
        else:
            error = 'Username not found'
            cur.close()
            return render_template("login.html", error=error)
    return render_template('login.html')


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == '__main__':
    app.secret_key = 'pass123'
    # Put debug = False in Production environment
    app.run(debug=True)
