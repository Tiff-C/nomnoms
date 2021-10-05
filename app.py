import os
from datetime import datetime
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env  # noqa

app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/all_recipes")
def all_recipes():
    """
    Gets all recipes and categories from db and renders all_recipes template
    """
    recipes = mongo.db.recipes.find()
    categories = list(mongo.db.categories.find())
    return render_template(
        "all_recipes.html", categories=categories, recipes=recipes)


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
        existing_user = mongo.db.users.find_one(
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
        mongo.db.users.insert_one(register)

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
        existing_user = mongo.db.users.find_one(
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
    categories = list(mongo.db.categories.find())

    if session["user"].lower() == username.lower():
        # find the session["user"]
        username = mongo.db.users.find_one({"username": username})
        # get list of users recipes
        user_recipes = username["user_recipes"]
        # grab only the recipes by this session["user"]
        recipes = mongo.db.recipes.find({"_id": {"$in": user_recipes}})

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
    categories = mongo.db.categories.find().sort("recipe_category", 1)
    cuisines = mongo.db.cuisines.find().sort("recipe_cuisine", 1)
    cooking_methods = mongo.db.cooking_methods.find().sort("cooking_method", 1)

    if request.method == "POST":
        date = datetime.now()
        user = mongo.db.users.find_one({"username": session["user"]})
        recipe = {
            "name": request.form.get("name"),
            "author": user["username"],
            "created_date": date,
            "prep_time": request.form.get("prep_time"),
            "cook_time": request.form.get("cook_time"),
            "cooking_method": request.form.get("cooking_method"),
            "recipe_category": request.form.get("recipe_category"),
            "recipe_cuisine": request.form.get("recipe_category"),
            "recipe_ingredient": request.form.getlist("recipe_ingredient"),
            "recipe_instructions": request.form.getlist(
                "recipe_instruction"),
            "recipe_yield": request.form.get("recipe_yield"),
            "recipe_image": request.form.get("recipe_image")
        }
        # stores the new ID for the recipe
        recipeId = mongo.db.recipes.insert_one(recipe)
        # pushes new recipe ID to the users "user_recipes"
        mongo.db.users.update_one(
            {"_id": ObjectId(user["_id"])},
            {"$push": {"user_recipes": recipeId.inserted_id}})
        flash("Recipe successfully added, thank you!")
        return redirect(url_for("my_recipes"))

    return render_template(
        "add_recipe.html",
        categories=categories,
        cuisines=cuisines,
        cooking_methods=cooking_methods)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
