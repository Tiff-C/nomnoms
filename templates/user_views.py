""" Import required modules """
from flask import (
    flash, render_template,
    redirect, request, session, url_for)
from werkzeug.security import generate_password_hash, check_password_hash


from app import app, db


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

        # app.add_url_rule('/register', 'register', register, methods=["GET", "POST"])
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


@app.route("/logout")
def logout():
    """
    Logs user out by removing user from session cookies.
    """
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")


    return redirect(url_for("login"))
