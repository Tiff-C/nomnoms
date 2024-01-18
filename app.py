""" Required imports """
import os
from datetime import datetime
from flask import (
    Flask, Blueprint, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from user_views import register_page, login_page, logout_page
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


# # the following try/except block is a way to verify that the database connection is alive (or not)
# try:
#     # verify the connection works by pinging the database
#     cxn.admin.command("ping")  # The ping command is cheap and does not require auth.
#     print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
# except Exception as e:
#     # the ping command failed, so the connection is not available.
#     print(" * MongoDB connection error:", e)  # debug

# imported routes
app.register_blueprint(register_page)
app.register_blueprint(login_page)
app.register_blueprint(logout_page)

# routes
@app.route("/")
@app.route("/all_recipes")
def all_recipes():
    """
    Gets all recipes and categories from db and renders all_recipes template
    """
    recipes = db.recipes.find()
    categories = list(db.categories.find())
    return render_template(
        "all_recipes.html", categories=categories, recipes=recipes) 


@app.route("/search", methods=["GET", "POST"])
def search():
    """ 
    Allows users to search recipies
    """
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
        recipe_id = db.recipes.insert_one(recipe)
        # pushes new recipe ID to the users "user_recipes"
        db.users.update_one(
            {"_id": ObjectId(user["_id"])},
            {"$push": {"user_recipes": recipe_id.inserted_id}})
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
    """
    Allows users to delete their own recipies
    """
    db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("my_recipes", username=session["user"]))


# run the app
if __name__ == "__main__":
    # use the PORT environment variable, or default to 5000
    FLASK_PORT = os.environ.get("FLASK_PORT", "5000")

    # import logging
    # logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(port=FLASK_PORT)
