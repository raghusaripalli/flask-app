from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':

    # Put debug = False in Production environment
    app.run(debug=True)
