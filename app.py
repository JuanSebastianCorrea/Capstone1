import os
import requests
from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserSignupForm, LoginForm, AddRecipe
from models import db, connect_db, User, Recipe, FavoriteRecipe
from search_service import search
from search_favorites_service import search_favorites
from search_own_service import search_own
from add_favorites_req_service import get_recipe

CURR_USER_KEY = "curr_user"

API_ID = '7ad5f5c3'
API_KEY = '75d853b05cbe14a1b05b4fd0c1f472bc'
BASE_URL = 'https://api.edamam.com/search?'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///recipes_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lindalindatonina')
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


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

#//////////////////////////////////////////////////#


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserSignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username or Email already registered", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)

#//////////////////////////////////////////////////#

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

    return render_template('login.html', form=form)

#//////////////////////////////////////////////////#

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/")

##############################################################################

@app.route('/')
def home():
    """Display Hompage"""

    curr_user = g.user
    return render_template('home.html', curr_user=curr_user)

#################### Favorites ###############################

@app.route('/favorites')
def view_favorites():
    """View user's favorite/saved recipes"""

    if not g.user:
        flash("Please log in first!", "danger")
        return redirect("/login")

    curr_user = User.query.get_or_404(g.user.id)
    favorites = curr_user.favorites

    return render_template('favorites.html', favorites=favorites)

@app.route('/favorites/add', methods=["POST"])
def add_favorite():
    """Add/Save recipe to user's Favorites page"""

    if not g.user:
        flash("Please log in first!", "danger")
        return redirect("/login")

    recipe_uri = request.form["add-favorite-input"]
    recipe_data = get_recipe(recipe_uri)
    
    # add selected recipe to DB if it does not already exist in DB
    recipe = Recipe.query.get(recipe_uri)
    if recipe == None:
        db_recipe = Recipe(uri=recipe_data[0]['uri'], name=recipe_data[0]['label'], image_url=recipe_data[0]['image'], url=recipe_data[0]['url'])
        db.session.add(db_recipe)
        db.session.commit()

    # add recipe to user's favorites
    new_fav = FavoriteRecipe(user_id=session[CURR_USER_KEY], recipe_uri=recipe_uri)
    db.session.add(new_fav)
    db.session.commit()
    flash(f"Recipe saved!", "success")
    return redirect('/favorites')

@app.route('/favorites/remove', methods=["POST"])
def remove_favorite():
    """Remove recipe from user's Favorites page"""

    if not g.user:
        flash("Please log in first!", "danger")
        return redirect("/login")

    curr_user = User.query.get_or_404(g.user.id)
    recipe_uri = request.form["remove-favorite-input"]

    FavoriteRecipe.query.filter((FavoriteRecipe.user_id == curr_user.id) & (FavoriteRecipe.recipe_uri == recipe_uri)).delete()
    db.session.commit()

    flash(f"Recipe removed!", "success")
    return redirect('/favorites')



#################### My Recipes ###############################
@app.route('/my_recipes')
def view_my_recipes():
    """View user's own recipes page"""

    if not g.user:
        flash("Please log in first!", "danger")
        return redirect("/login")

    my_recipes = Recipe.query.filter(Recipe.user_id==g.user.id).all()
    return render_template('my-recipes.html', my_recipes=my_recipes)

@app.route('/my_recipes/add_recipe', methods=["GET", "POST"])
def add_recipe():
    """Add new own recipe for current user.
       Get and Submit recipe form.
    """

    if not g.user:
        flash("Please log in first!", "danger")
        return redirect("/login")
    user_id = g.user.id
    
    form = AddRecipe(user_id=user_id)
    
    if form.validate_on_submit():
        
        new_recipe = Recipe(uri=form.name.data,
                            name=form.name.data,
                            image_url=form.image_url.data if form.image_url.data != "" else "/static/images/defaultfood.png",
                            cuisine_type=form.cuisine_type.data,
                            ingredients=form.ingredients.data,
                            instructions=form.instructions.data,
                            user_id=user_id)

        db.session.add(new_recipe)
        db.session.commit()


        flash(f"Your recipe has been added!", "success")
        return redirect("/my_recipes")

    return render_template('add-recipe.html', form=form)

@app.route('/my_recipes/delete', methods=["POST"])
def delete_my_recipe():
    """Delete user's own recipe"""

    if not g.user:
        flash("Please log in first!", "danger")
        return redirect("/login")

    curr_user = User.query.get_or_404(g.user.id)
    recipe_uri = request.form.get("delete-my-recipe-input")

    Recipe.query.filter((Recipe.user_id == curr_user.id) & (Recipe.uri == recipe_uri)).delete()
    db.session.commit()
    flash(f"Recipe deleted!", "success")
    return redirect('/my_recipes')

@app.route('/my_recipes/<recipe_uri>')
def view_recipe(recipe_uri):
    """Display full recipe for user's own recipe"""

    if not g.user:
        flash("Please log in first!", "danger")
        return redirect("/login")

    my_recipe = Recipe.query.filter((Recipe.user_id==g.user.id)&(Recipe.uri==recipe_uri)).first()
    ingredients_list = my_recipe.ingredients.split(',')
    steps = my_recipe.instructions.split(',')

    return render_template('full-recipe.html', my_recipe=my_recipe, ingredients_list=ingredients_list, steps=steps)

@app.route('/my_recipes/<recipe_uri>/edit', methods=["GET", "POST"])
def edit_my_recipe(recipe_uri):
    """Edit user's own recipe.
       Get and submit edit form
    """

    if not g.user:
        flash("Please log in first!", "danger")
        return redirect("/login")

    user_id = g.user.id
    recipe = Recipe.query.get_or_404(recipe_uri)

    form = AddRecipe(user_id=user_id, obj=recipe)

    if form.validate_on_submit():

        recipe.name = form.name.data
        recipe.image_url = form.image_url.data
        recipe.cuisine_type = form.cuisine_type.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        
        db.session.commit()
        return redirect(f'/my_recipes/{recipe.uri}')
    
    return render_template('edit-recipe.html', form=form, recipe=recipe)


##################### GENERAL SEARCH TO EXTERNAL API ################################

@app.route('/search_api')
def search_api():
    """Search for recipes"""   

    searchterm = request.args["searchterm"]
    frm = request.args["frm"]
    to = request.args["to"]

    user_id = g.user.id if g.user else None
    recipes_list = search(user_id, searchterm, frm, to)
    return jsonify(recipes_list)


##################### SEARCH DB ################################
@app.route('/get_favorites/<searchterm>')
def get_favorites(searchterm):
    """Search Favorites searchbar. 
        Display favorited recipes that match searchterm real-time.
    """

    if not g.user:
        flash("Unauthorized page! Must be logged in!", 'danger') 
        return redirect('/login')   
    else:
        user_id = g.user.id 

        serialized_favs = search_favorites(user_id, searchterm)
    
        return jsonify(serialized_favs)


@app.route('/get_own/<searchterm>')
def get_own(searchterm):
    """Search Own Recipes searchbar. 
        Display own recipes that match searchterm real-time.
    """

    if not g.user:
        flash("Unauthorized page! Must be logged in!", 'danger') 
        return redirect('/login')   
    else:
        user_id = g.user.id 

        serialized_own = search_own(user_id, searchterm)
    
        return jsonify(serialized_own)

 