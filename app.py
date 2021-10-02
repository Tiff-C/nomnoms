import os
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
    use. If username exists user is redirected to register page. If username
    doesn't exist it will insert register dict into database then put user
    into a session and redirect to my_recipes.
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
    user into session with welcome message. If password is incorrect / user
    does not exist; flashes message to user and redirects to login.
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
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
