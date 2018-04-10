import datetime
import os

from flask import Flask, render_template, redirect, url_for, request, jsonify
from models import Committee, Hearing, Speech, Speaker, Congressmember, Constituency
from database import db_session

app = Flask(__name__)
# app.secret_key = os.environ['APP_SECRET_KEY']

class Query():
    def __init__(self):
        self.committees = None
        self.parties = None
        self.data = []

class Records():
    def __init__(self):
        self.no_of_records = 0
        self.data = []

    def update_data(self, data):
        self.data = data
        self.no_of_records = len(data)


def get_committee_query(committee_id, surname, party, district):

    data = db_session.query(Hearing, Speech, Speaker, Congressmember, Constituency)

    if committee_id:
        committee_id = int(committee_id)
        data = data.filter(Hearing.committee_id == committee_id)

    if surname:
        surname = surname.lower()
        data = data.filter(Speaker.surname == surname)

    if party:
        data = data.filter(Congressmember.party == party)

    if district:
        data = data.filter(Constituency.district == district)

    data = data.filter(Hearing.hearing_id == Speech.hearing_id)
    data = data.filter(Speech.speech_id == Speaker.speech_id)
    data = data.filter(Speaker.person_id == Congressmember.person_id)
    data = data.filter(Congressmember.constituency_id == Constituency.constituency_id)


    data = data.with_entities(Hearing.hearing_title, Hearing.date, Speaker.surname, Speech.text).distinct().all()

    return data


@app.route("/", methods=['GET', 'POST'])
def index():
    query = Query()
    records = Records()

    # TODO: currently quering only options that HAVE hearings in small database. can query all once we have full db.
    committees = db_session.query(Committee, Hearing)
    committees = committees.filter(Hearing.committee_id == Committee.committee_id)
    committees = committees.with_entities(Committee.committee_id, Committee.committee_name).distinct().all()
    query.committees = committees

    parties = db_session.query(Hearing, Speech, Speaker, Congressmember)
    parties = parties.filter(Congressmember.person_id == Speaker.person_id)
    parties = parties.filter(Speaker.speech_id == Speech.speech_id)
    parties = parties.filter(Speech.hearing_id == Hearing.hearing_id)
    parties = parties.with_entities(Congressmember.party).distinct().all()
    query.parties = parties

    if request.method == 'POST':
        committee_id = request.form.get('committee')
        surname = request.form.get('surname')
        party = request.form.get('party')
        district = request.form.get('district')
        records.update_data(get_committee_query(committee_id, surname, party, district))

    return render_template('index.html', query=query, records=records)

@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
