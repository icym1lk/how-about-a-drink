import os
import requests
# import Flask and any libraries you want to use
from flask import Flask, request, jsonify, render_template, redirect, flash, session, g
from sqlalchemy.exc import IntegrityError
# get db related stuff from models.py
from models import db, connect_db, User, Favorite, Drink
# get forms from forms.py
from forms import SearchAPIForm, UserAddForm, UserEditForm, LoginForm

CURR_USER_KEY = "curr_user"

# instantiate and instance of Flask. app is standard name
app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///drinks_db'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

# connect to db
connect_db(app)

app.config["SECRET_KEY"] = "secret"

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
          
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()
    
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    # IMPLEMENT THIS
    user = User.query.get(session[CURR_USER_KEY])
    flash(f'Goodbye {user.username}', "info")
    do_logout()
    return redirect("/")

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
  
        # send query for cocktail or letter/number
        else:
            res = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?',
                                params = {query_type: query})
        
        # check if data was found, if no data found notify user
        if res.text == '':
            flash("No results found.", "info")
            return redirect("/")

        data = res.json()

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

    return render_template("results.html", form=form, data=data)

##############################################################################
# General user routes:

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)
    favorited = [f.id for f in user.favorites]
    favorited_drinks = Drink.query.filter(Drink.id.in_(favorited)).all()
    
    return render_template('users/show.html', user=user, form=form, favorited_drinks=favorited_drinks)
    
@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data

            db.session.add(user)
            db.session.commit()
            return redirect(f"/users/{user.id}")

        flash("Incorrect password entered. Please try again.", "danger")

    return render_template("/users/edit.html", form=form, user=user)

@app.route('/users/favorite/<int:drink_id>', methods=["GET", "POST"])
def add_favorite(drink_id):
    """Favorite drink with current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    new_drink = Drink(id=drink_id)
    db.session.add(new_drink)
    db.session.commit()
    
    favorited = [f.id for f in user.favorites]
    favorited_drinks = Drink.query.filter(Drink.id.in_(favorited)).all()
    
    if drink_id in favorited:
        favorite = Favorite.query.filter(Favorite.user_id == user.id, Favorite.drink_id == drink_id).first()
        db.session.delete(favorite)
        db.session.commit()
        return redirect("/")
        
    new_favorite = Favorite(user_id=g.user.id, drink_id=drink_id)
    db.session.add(new_favorite)
    db.session.commit()

    return redirect("/")

@app.route('/users/<int:user_id>/favorites')
def users_favorites(user_id):
    """Show list of favorites of this user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    favorited = [f.id for f in user.favorites]
    favorited_drinks = Drink.query.filter(Drink.id.in_(favorited)).all()
    return render_template("/users/likes.html", user=user, favorited_drinks=favorited_drinks)

@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    name = g.user.username
    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    flash(f"User {name} deleted.", "danger")
    return redirect("/signup")