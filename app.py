import datetime
import os

from flask import Flask, render_template, redirect, url_for, request, jsonify
from models import Committee, Hearing, Speech, Speaker
from database import db_session

app = Flask(__name__)
# app.secret_key = os.environ['APP_SECRET_KEY']


class Query():
    def __init__(self):
        self.committees = None
        self.data = []


class Records():
    def __init__(self):
        self.no_of_records = 0
        self.data = []

    def update_data(self, data):
        self.data = data
        self.no_of_records = len(data)


@app.route("/", methods=['GET', 'POST'])
def index():
    query = Query()
    records = Records()

    committees = db_session.query(Committee, Hearing)
    committees = committees.filter(Hearing.committee_id == Committee.committee_id)
    committees = committees.with_entities(Committee.committee_id, Committee.committee_name).distinct().all()
    query.committees = committees

    if request.method == 'POST':
        committee_id = request.form.get('committee_id')
        records.data = get_committee_query(committee_id)

    return render_template('index.html', query=query, records=records)


def get_committee_query(committee_id):
    if committee_id:
        committee_id = int(committee_id)
        committees = db_session.query(Hearing, Speech, Speaker)
        committees = committees.filter(Hearing.committee_id == committee_id)
        committees = committees.filter(Speech.hearing_id == Hearing.hearing_id)
        committees = committees.filter(Speaker.speech_id == Speech.speech_id)
        committees = committees.with_entities(Hearing.hearing_title, Hearing.date, Speech.text, Speaker.surname,
                                              Hearing.committee_id).all()
    else:
        committees = db_session.query(Hearing, Speech, Speaker)
        committees = committees.filter(Speech.hearing_id == Hearing.hearing_id)
        committees = committees.filter(Speaker.speech_id == Speech.speech_id)
        committees = committees.with_entities(Hearing.hearing_title, Hearing.date, Speech.text, Speaker.surname,
                                              Hearing.committee_id).all()

    return committees


@app.route("/person")
def person():
    return render_template('person.html')


@app.route("/party")
def party():
    return render_template('party.html')


@app.route("/district")
def district():
    return render_template('district.html')


# DEPRECATED after I implemented the Committee option in All queries
@app.route('/committee', methods=['GET', 'POST'])
def committee():
    if request.method == 'POST':
        committee_id = request.form.get('committee_id')
        if committee_id:
            committee_id = int(committee_id)
            data = (db_session.query(Hearing, Speech, Speaker
                                     ).filter(Hearing.committee_id == committee_id
                                              ).filter(Speech.hearing_id == Hearing.hearing_id
                                                       ).filter(Speaker.speech_id == Speech.speech_id
                                                                ).with_entities(Hearing.hearing_title, Hearing.date,
                                                                                Speech.text, Speaker.surname,
                                                                                Hearing.committee_id)).all()
        else:
            data = (db_session.query(Hearing, Speech, Speaker
                                     ).filter(Speech.hearing_id == Hearing.hearing_id
                                              ).filter(Speaker.speech_id == Speech.speech_id
                                                       ).with_entities(Hearing.hearing_title, Hearing.date, Speech.text,
                                                                       Speaker.surname, Hearing.committee_id)).all()

    else:
        data = {};

    no_of_records = len(data)
    committees = db_session.query(Committee, Hearing
                                  ).filter(Hearing.committee_id == Committee.committee_id
                                           ).with_entities(Committee.committee_id,
                                                           Committee.committee_name).distinct().all()
    return render_template('committee.html', committees=committees, data=data, no_of_records=no_of_records)


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
