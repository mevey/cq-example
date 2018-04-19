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


def get_records(committee_name, name, party, chamber, district, state, year, quintile):

    data = db_session.query(Speech)\
                    .join(Hearing, Hearing.hearing_id == Speech.hearing_id)\
                    .join(Speaker, Speech.speech_id == Speaker.speech_id)\
                    .join(Congressmember, Speaker.person_id == Congressmember.person_id, isouter=True)\
                    .join(Committee, Committee.committee_id == Hearing.committee_id, isouter=True)\
                    .join(Person, Person.person_id == Speaker.person_id)\
                    .join(Constituency, Constituency.constituency_id == Congressmember.constituency_id, isouter=True)\
                    .join(ConstituencyCharacteristics, ConstituencyCharacteristics.constituency_id == Constituency.constituency_id, isouter=True)

    if committee_name:
        data = data.filter(Committee.committee_name == committee_name)

    if name:
        name = name.lower()
        data = data.filter(Person.full_name.like("%"+ name +"%"))

    if party:
        data = data.filter(Congressmember.party == party)

    if chamber:
        data = data.filter(Congressmember.chamber == chamber)

    if year:
        data = data.filter(Hearing.date.like("%"+ year +"%"))

    if district:
        data = data.filter(Constituency.district == district)

    if state:
        data = data.filter(Constituency.state_name == state)

    if quintile:
        data = data.filter(ConstituencyCharacteristics.density_quintile == quintile)

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
    print(data.statement)
    return data

def get_count(committee_name, name, party, chamber, district, state, year, quintile):

    data = db_session.query(Speech)\
                    .join(Hearing, Hearing.hearing_id == Speech.hearing_id)\
                    .join(Speaker, Speech.speech_id == Speaker.speech_id)\
                    .join(Congressmember, Speaker.person_id == Congressmember.person_id, isouter=True)\
                    .join(Committee, Committee.committee_id == Hearing.committee_id, isouter=True)\
                    .join(Person, Person.person_id == Speaker.person_id)\
                    .join(Constituency, Constituency.constituency_id == Congressmember.constituency_id, isouter=True)\
                    .join(ConstituencyCharacteristics, ConstituencyCharacteristics.constituency_id == Constituency.constituency_id, isouter=True)

    if committee_name:
        data = data.filter(Committee.committee_name == committee_name)

    if name:
        name = name.lower()
        data = data.filter(Person.full_name.like("%"+ name +"%"))

    if party:
        data = data.filter(Congressmember.party == party)

    if chamber:
        data = data.filter(Congressmember.chamber == chamber)

    if year:
        data = data.filter(Hearing.date == year)

    if district:
        data = data.filter(Constituency.district == district)

    if state:
        data = data.filter(Constituency.state_name == state)

    if quintile:
        data = data.filter(ConstituencyCharacteristics.density_quintile == quintile)

    return data.count()


@app.route("/", methods=['GET', 'POST'])
def index():
    query = Query()
    records = Records()

    committee_name = request.form.get('committee',"")
    name = request.form.get('name',"")
    party = request.form.get('party')
    chamber = request.form.get('chamber')
    district = request.form.get('district')
    state = request.form.get('state')
    year = request.form.get('year')
    quintile = request.form.get('quintile')

    records.update_data(get_records(committee_name, name, party, chamber, district, state, year, quintile))
    count = get_count(committee_name, name, party,chamber, district, state, year, quintile)

    selected = {
            "committee_name": committee_name,
            "name": name,
            "party": party,
            "district": district,
            "state": state,
            "year": year,
            "quintile": quintile,
        }
    years = [str(x) for x in range(2018, 1997, -1)]
    return render_template('index.html', query=query, records=records, selected=selected, count=count, years=years)

@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
