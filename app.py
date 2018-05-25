import datetime
import os,csv, sqlite3

from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file
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

"""
I Know, I know. I a mixing sqlalchemy up with raw sql. I just needed to add this functionality fast.
Plus, the first rule in engineering is that the it should work!
"""

@app.route('download/')
def download():
    committee_name = request.form.get('committee',"")
    name = request.form.get('name',"")
    party = request.form.get('party')
    chamber = request.form.get('chamber')
    district = request.form.get('district')
    state = request.form.get('state')
    year = request.form.get('year')
    quintile = request.form.get('quintile')

    connection = sqlite3.connect("cq_180410.sqlite")
    connection.row_factory = dictionary_factory
    cursor = connection.cursor()

    # Query that gets the records that match the query
    all_records_query = """SELECT full_name,honorific,text,hearing_title,year,committee_name,type,party,chamber,state_name,district
        FROM capitolquery %s %s;"""

    where_clause = ""
    where_clause_arr = []
    conditions_tuple = []
    if name or year or party or state or committee_name or quintile or chamber or district:
        if name:
            where_clause_arr.append(" capitolquery.full_name like ? ")
            conditions_tuple.append("%" + name + "%")
        if year:
            where_clause_arr.append(" capitolquery.year = ?")
            conditions_tuple.append(year)
        if party:
            where_clause_arr.append(" capitolquery.party = ? ")
            conditions_tuple.append(party)
        if state:
            where_clause_arr.append(" capitolquery.state_name = ? ")
            conditions_tuple.append(state)
        if chamber:
            where_clause_arr.append(" capitolquery.chamber = ? ")
            conditions_tuple.append(state)
        if quintile:
            where_clause_arr.append(" capitolquery.density_quintile = ? ")
            conditions_tuple.append(quintile)
        if district:
            where_clause_arr.append(" capitolquery.district = ? ")
            conditions_tuple.append(district)
        if committee_name:
            where_clause_arr.append(" capitolquery.committee_name = ? ")
            conditions_tuple.append(committee_name)
        where_clause = "where " + ("and".join(where_clause_arr))

    limit_statement = "" #"limit 10" if format_ != "csv" else ""

    all_records_query = all_records_query % (where_clause, limit_statement)

    conditions_tuple = tuple(conditions_tuple)
    cursor.execute(all_records_query, conditions_tuple)
    records = cursor.fetchall()

    connection.close()

    return download_csv(records, "speeches.csv")



########################################################################
# The following are helper functions. They do not have a @app.route decorator
########################################################################
def dictionary_factory(cursor, row):
    """
    This function converts what we get back from the database to a dictionary
    """
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]
    return d


def download_csv(data, filename):
    """
    Pass into this function, the data dictionary and the name of the file and it will create the csv file and send it to the view
    """
    header = data[0].keys()  # Data must have at least one record.
    with open('downloads/' + filename, "w+") as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        for row in data:
            writer.writerow(list(row.values()))

    # Push the file to the view
    return send_file('downloads/' + filename,
                     mimetype='text/csv',
                     attachment_filename=filename,
                     as_attachment=True)


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
