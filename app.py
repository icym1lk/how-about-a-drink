import requests
# import Flask and any libraries you want to use
from flask import Flask, request, jsonify, render_template, redirect, flash, session
# get db related stuff from models.py
from models import db, connect_db
# get forms from forms.py
from forms import SearchAPIForm

# instantiate and instance of Flask. app is standard name
app = Flask(__name__)

# connect to db
connect_db(app)

app.config["SECRET_KEY"] = "secret"

@app.route("/")
def homepage():
    """Show homepage."""
    form = SearchAPIForm()

    return render_template("index.html", form=form)

@app.route("/results", methods=["GET", "POST"])
def search_results():
    """Render search results."""
    form = SearchAPIForm()
    if form.validate_on_submit():
        query_type = form.query_type.data
        query = form.query.data
        # print(f"{query_type}*********{query}")

        # check if query was for letter/number.
        # These queries cannot be more than 1 character.
        if query_type == 'f':
            if len(query) > 1:
                flash("Please select 1 letter or 1 number for that search type.", "danger")
                return redirect("/")
        # check if query was for ingredient
        # ingredient API call is different end point than cocktail and letter/number
        if query_type == 'i':
            res = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?',
                                params = {query_type: query})
            # print(f"**********************{res}")
            # import pdb
            # pdb.set_trace()
        # send query for cocktail or letter/number
        else:
            res = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?',
                                params = {query_type: query})
        if res.text == '':
            flash("No results found.", "info")
            return redirect("/")

        data = res.json()
        # import pdb
        # pdb.set_trace()
        # print(f"#########################################{data}")
        # check if data was found, if no data found notify user
        if data['drinks'] == None:
            flash("No results found.", "info")
            return redirect("/")
        else:
            return render_template("results.html", form=form, data=data, query=query, query_type=query_type)
    else:
        return redirect("/")

@app.route("/random", methods=["GET", "POST"])
def random_cocktail():
    """Render random cocktail results."""

    form = SearchAPIForm()
    
    res = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    data = res.json()
    # print(data)

    return render_template("results.html", form=form, data=data)