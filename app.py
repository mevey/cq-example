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
    return render_template('speaker.html')

@app.route("/all")
def all():
    #takes care of the big query
    committees = db_session.query(Committee).all() # or you could have used User.query.all()
    return render_template('query.html', committees=committees)

@app.route("/persom")
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
