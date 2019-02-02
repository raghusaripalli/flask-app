from flask import Flask, render_template
from data import Articles

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


if __name__ == '__main__':

    # Put debug = False in Production environment
    app.run(debug=True)
