import datetime
import os

from flask import Flask, render_template, redirect, url_for, request, jsonify
from models import CapitolQuery
from database import db_session
from sqlalchemy import func, inspect

app = Flask(__name__)


def object_as_dict(obj):
    for c in inspect(obj)._entities:
        print(dir(c))
        break

    return {c.key: getattr(obj, c.key)
            for c in inspect(obj)._entities}

def get_records(committee_name, name, party, chamber, district, state, year, quintile):

    data = db_session.query(CapitolQuery)
    data = add_filters(data, committee_name, name, party, chamber, district, state, year, quintile)

    data = data.with_entities(
        CapitolQuery.honorific,
        CapitolQuery.full_name,
        CapitolQuery.text,
        CapitolQuery.hearing_title,
        CapitolQuery.date,
        CapitolQuery.committee_name,
        CapitolQuery.type,
        CapitolQuery.party,
        CapitolQuery.chamber,
        CapitolQuery.state_name,
        CapitolQuery.district,
        CapitolQuery.density_quintile
    ).limit(10)

    return data.all()

def add_filters(data, committee_name, name, party, chamber, district, state, year, quintile):
    if committee_name:
        data = data.filter(CapitolQuery.committee_name == committee_name.strip())

    if name:
        name = name.lower()
        data = data.filter(CapitolQuery.full_name.like("%"+ name.strip() +"%"))

    if party:
        data = data.filter(CapitolQuery.party == party)

    if chamber:
        data = data.filter(CapitolQuery.chamber == chamber)

    if year:
        data = data.filter(CapitolQuery.year == year)

    if district:
        data = data.filter(CapitolQuery.district == district)

    if state:
        data = data.filter(CapitolQuery.state_name == state)

    if quintile:
        data = data.filter(CapitolQuery.density_quintile == quintile)
    return data

def get_count(committee_name, name, party, chamber, district, state, year, quintile):
    data = db_session.query(CapitolQuery.id)
    data = add_filters(data, committee_name, name, party, chamber, district, state, year, quintile)

    return data.count()

@app.route("/")
def index():
    years = [str(x) for x in range(2018, 1996, -1)]
    return render_template('index.html', years=years)

@app.route("/records", methods=['GET', 'POST'])
def records():
    committee_name = request.form.get('committee',"")
    name = request.form.get('name',"")
    party = request.form.get('party')
    chamber = request.form.get('chamber')
    district = request.form.get('district')
    state = request.form.get('state')
    year = request.form.get('year')
    quintile = request.form.get('quintile')

    s = datetime.datetime.now()
    records = get_records(committee_name, name, party, chamber, district, state, year, quintile)
    e = datetime.datetime.now()
    print((e-s).total_seconds())
    s = datetime.datetime.now()
    count = get_count(committee_name, name, party,chamber, district, state, year, quintile)
    e = datetime.datetime.now()
    print((e - s).total_seconds())

    return jsonify( records = list(records), count=count)

@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
