import os
from datetime import datetime
from flask import (
    Flask, flash, render_template, current_app, g,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env  # noqa


# instantiate the app
app = Flask(__name__)


# turn on debugging if in development mode
if os.environ.get("FLASK_ENV", "development") == "development":
    # turn on debugging, if in development
    app.debug = os.environ.get("DEBUG")  # debug mnode


# connect to the database
cxn = MongoClient(os.environ.get("DB_URI"))
db = cxn[os.environ.get("MONGO_DBNAME")]  # store a reference to the database


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


# the following try/except block is a way to verify that the database connection is alive (or not)
try:
    # verify the connection works by pinging the database
    cxn.admin.command("ping")  # The ping command is cheap and does not require auth.
    print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(" * MongoDB connection error:", e)  # debug


# set up the routes


@app.route("/")
@app.route("/all_recipes")
def all_recipes():
    """
    Gets all recipes and categories from db and renders all_recipes template
    """
    try:
        recipes = db.recipes.find()
        categories = list(db.categories.find())
        return render_template(
            "all_recipes.html", categories=categories, recipes=recipes) 
    except: 
        print ("Error getting recipies")
        return render_template("error.html") 


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = db.recipes.find({"$text": {"$search": query}})
    return render_template("all_recipes.html", recipes=recipes)


@app.route("/category/<recipe_category>")
def category(recipe_category):
    """
    Renders the recipe category template.
    """
    category = recipe_category
    recipes = list(db.recipes.find({"recipe_category": recipe_category}))

    return render_template("category.html", recipes=recipes, category=category)


@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
    """
    Renders the recipe template.
    """
    recipe = db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = list(db.categories.find())

    return render_template("recipe.html", recipe=recipe, categories=categories)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    If the request method is post it will check if the username is already in
    use.
    If username exists user is redirected to register page.
    If username doesn't exist it will insert register dict into database
    then put user into a session and redirect to my_recipes.
    """
    if request.method == "POST":
        # check if username already exists in db
        existing_user = db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "superuser": "False",
            "user_recipes": [],
            "user_favourites": []
        }
        db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("all_recipes", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Renders login template, if method is post it checks if user exists.
    If user exists it checks the password, if the password is correct; puts
    user into session with welcome message.
    If password is incorrect / user does not exist; flashes message to user
    and redirects to login.
    """
    if request.method == "POST":
        # Check if username exists in db
        existing_user = db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get(
                    "username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "my_recipes", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/my_recipes/<username>", methods=["GET", "POST"])
def my_recipes(username):
    """
    User will be redirected to this page on login.
    If the session username matches the route username; it will find the
    session["user"] and store the user_recipes ID's.
    It then searches MongoDB for the recipes and renders my_recipes template.
    If a user tries to access another users my_recipes page they will be
    redirected to their own my_recipes page.
    """
    # get categories for recipes with no img URL
    categories = list(db.categories.find())

    if session["user"].lower() == username.lower():
        # find the session["user"]
        username = db.users.find_one({"username": username})
        # get list of users recipes
        user_recipes = username["user_recipes"]
        # grab only the recipes by this session["user"]
        recipes = db.recipes.find({"_id": {"$in": user_recipes}})

        return render_template(
            "my_recipes.html",
            username=username,
            categories=categories,
            recipes=recipes)

    # take the incorrect user to their own profile
    return redirect(url_for("my_recipes", username=session["user"]))


@app.route("/logout")
def logout():
    """
    Logs user out by removing user from session cookies.
    """
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    """
    Renders add_recipe template. If method is post; stores form input from
    user in recipe dict, inserts recipe into db, pushes the new recipe ID
    to the users "user_recipes" array then redirects to my_recipes.
    """
    categories = db.categories.find().sort("recipe_category", 1)
    cuisines = db.cuisines.find().sort("recipe_cuisine", 1)
    cooking_methods = db.cooking_methods.find().sort("cooking_method", 1)

    if request.method == "POST":
        date = datetime.now()
        user = db.users.find_one({"username": session["user"]})
        recipe = {
            "name": request.form.get("name"),
            "author": user["username"],
            "created_date": date,
            "prep_time": request.form.get("prep_time"),
            "cook_time": request.form.get("cook_time"),
            "cooking_method": request.form.getlist("cooking_method"),
            "recipe_category": request.form.get("recipe_category"),
            "recipe_cuisine": request.form.get("recipe_cuisine"),
            "recipe_ingredient": request.form.getlist("recipe_ingredient"),
            "recipe_instructions": request.form.getlist(
                "recipe_instruction"),
            "recipe_yield": request.form.get("recipe_yield"),
            "recipe_image": request.form.get("recipe_image")
        }
        # stores the new ID for the recipe
        recipeId = db.recipes.insert_one(recipe)
        # pushes new recipe ID to the users "user_recipes"
        db.users.update_one(
            {"_id": ObjectId(user["_id"])},
            {"$push": {"user_recipes": recipeId.inserted_id}})
        flash("Recipe successfully added, thank you!")
        return redirect(url_for("my_recipes", username=session["user"]))

    return render_template(
        "add_recipe.html",
        categories=categories,
        cuisines=cuisines,
        cooking_methods=cooking_methods)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """
    Allows users to edit their added recipes.
    Gets recipe ID and all categories, cuisines and cooking_methods and passes
    this to the template.
    If the request method is post it will update the recipe in MongoDB.
    """
    categories = db.categories.find().sort("recipe_category", 1)
    cuisines = db.cuisines.find().sort("recipe_cuisine", 1)
    cooking_methods = db.cooking_methods.find().sort("cooking_method", 1)
    recipe = db.recipes.find_one({"_id": ObjectId(recipe_id)})

    if request.method == "POST":
        submit = {
            "name": request.form.get("name"),
            "prep_time": request.form.get("prep_time"),
            "cook_time": request.form.get("cook_time"),
            "cooking_method": request.form.getlist("cooking_method"),
            "recipe_category": request.form.get("recipe_category"),
            "recipe_cuisine": request.form.get("recipe_cuisine"),
            "recipe_ingredient": request.form.getlist("recipe_ingredient"),
            "recipe_instructions": request.form.getlist(
                "recipe_instruction"),
            "recipe_yield": request.form.get("recipe_yield"),
            "recipe_image": request.form.get("recipe_image")
        }
        db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        flash("Recipe Successfully Updated")
        return redirect(url_for("my_recipes", username=session["user"]))

    return render_template(
        "edit_recipe.html",
        recipe=recipe,
        categories=categories,
        cuisines=cuisines,
        cooking_methods=cooking_methods)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("my_recipes", username=session["user"]))


# route to handle any errors
@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template("error.html", error=e)  # render the edit template


# run the app
if __name__ == "__main__":
    # use the PORT environment variable, or default to 5000
    FLASK_PORT = os.environ.get("FLASK_PORT", "5000")

    # import logging
    # logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(port=FLASK_PORT)