import datetime
import os

from flask import Flask, render_template, redirect, url_for, request, jsonify
from models import Committee, Hearing, Speech, Speaker, Congressmember, Constituency, Person, ConstituencyCharacteristics
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
        self.no_of_records = 0#len(data)


def get_committee_query(committee_name, surname, party, district, state, year, quintile):

    data = db_session.query(Hearing, Speech, Speaker, Person, Committee,  Congressmember, Constituency, ConstituencyCharacteristics)

    if committee_name:
        data = data.filter(Committee.committee_name == committee_name)

    if surname:
        surname = surname.lower()
        data = data.filter(Speaker.surname == surname) #Note.message.like("%somestr%")

    if party:
        data = data.filter(Congressmember.party == party)

    if year:
        data = data.filter(Hearing.date == year)

    if district:
        data = data.filter(Constituency.district == district)

    if state:
        data = data.filter(Constituency.state_name == state)

    if quintile:
        data = data.filter(ConstituencyCharacteristics.density_quintile == quintile)

    data = data.filter(Hearing.hearing_id == Speech.hearing_id)
    data = data.filter(Speech.speech_id == Speaker.speech_id)
    data = data.filter(Speaker.person_id == Congressmember.person_id)
    data = data.filter(Committee.committee_id == Hearing.committee_id)
    data = data.filter(Person.person_id == Speaker.person_id)
    data = data.filter(Congressmember.person_id == Person.person_id)
    data = data.filter(Constituency.constituency_id == Congressmember.constituency_id)
    data = data.filter(ConstituencyCharacteristics.constituency_id == Constituency.constituency_id)


    data = data.with_entities(
        Hearing.hearing_title,
        Hearing.date,
        Hearing.url,
        Speaker.surname,
        Speech.text,
        Person.full_name,
        Person.honorific,
        Committee.committee_name,
        Committee.type,
        Congressmember.party,
        Congressmember.chamber,
        Constituency.district,
        Constituency.state_name,
        ConstituencyCharacteristics.density_quintile
    ).limit(10)

    return data


@app.route("/", methods=['GET', 'POST'])
def index():
    query = Query()
    records = Records()

    committee_name = request.form.get('committee')
    surname = request.form.get('surname')
    party = request.form.get('party')
    district = request.form.get('district')
    state = request.form.get('state')
    year = request.form.get('year')
    quintile = request.form.get('quintile')
    records.update_data(get_committee_query(committee_name, surname, party, district, state, year, quintile))

    return render_template('index.html', query=query, records=records)

@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
