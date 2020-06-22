import requests
# import Flask and any libraries you want to use
from flask import Flask, request, jsonify, render_template, redirect, flash, session
# get db related stuff from models.py
from models import db, connect_db

# instantiate and instance of Flask. app is standard name
app = Flask(__name__)

# connect to db
connect_db(app)

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")

@app.route("/results")
def search_results():
    """Render search results."""
    query = request.args['query']
    res = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?',
                                params = {'f': query})
    data = res.json()
    # import pdb
    # pdb.set_trace()
    print(data)

    return render_template("results.html", data=data)