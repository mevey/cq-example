import datetime
import os

from flask import Flask, render_template, redirect, url_for

from models import Committee
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/")
def query():
    committees = db_session.query(Committee).all() # or you could have used User.query.all()
    return render_template('query.html', committees=committees)

@app.route("/success")
def success():
    return "Thank you!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
