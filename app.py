import requests
# import Flask and any libraries you want to use
from flask import Flask, request, jsonify, render_template, redirect, flash, session
# get db related stuff from models.py
from models import db, connect_db

# instantiate and instance of Flask. app is standard name
app = Flask(__name__)

# connect to db
connect_db(app)

app.config["SECRET_KEY"] = "secret"

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")

@app.route("/results", methods=["POST"])
def search_results():
    """Render search results."""
    query_type = request.form['query_type']
    query = request.form['query']
    
    res = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?',
                                params = {query_type: query})
    data = res.json()
    # import pdb
    # pdb.set_trace()
    # print(f"#########################################{data}")

    if query_type == 'i':
        if data['ingredients'] == None:
            flash("No results found.")
            return redirect("/")
        else:
            return render_template("results.html", data=data, query=query, query_type=query_type)
    else:
        if data['drinks'] == None:
            flash("No results found.")
            return redirect("/")
        else:
            return render_template("results.html", data=data, query=query, query_type=query_type)