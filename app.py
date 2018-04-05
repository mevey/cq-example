import datetime
import os

from flask import Flask, render_template, redirect, url_for

from models import Committee
from database import db_session

app = Flask(__name__)
#app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/")
def index():
    committees = db_session.query(Committee).all()
    return render_template('index.html', committees=committees)

@app.route("/person")
def person():
    return render_template('person.html')

@app.route("/party")
def party():
    return render_template('party.html')

@app.route("/district")
def district():
    return render_template('district.html')

@app.route("/committee")
def committee():
    return render_template('committee.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
