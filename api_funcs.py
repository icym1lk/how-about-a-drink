import requests
from forms import SearchAPIForm
from flask import render_template

def callAPI(id):

    form = SearchAPIForm()

    res = requests.get('https://www.thecocktaildb.com/api/json/v1/1/lookup.php?',
                        params = {'i': id})
    data = res.json()

    return render_template("results.html", form=form, data=data)