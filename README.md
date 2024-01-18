# NomNoms 

> "Cooking made simple"

View the live project [here](https://nom-nom-s.herokuapp.com/)

## UX

### Project Goals

   This project is my third Milestone Project, the purpose of this project is to demonstrate the skills and knowledge I have developed during the Python Essentials and Backend Development modules. I have chosen project idea 1 - create an online cookbook.

   This cookbook will be a collection of simple homemade recipes initially from myself but hopefully in time they will be from around the world. It will be targeted at people who are looking for easy meal ideas that taste great! 
   Large recipe databases such as [BBC Good Food]() or [The Food Network]() are full of things you might want to try for your next dinner party but not too many things you can whip up in 30 mins using basic cupboard supplies or even using food from the freezer. Nothing fancy just simple food that tastes good.
   The intended users of the app range from parents looking for meal ideas for their weekly shop, young adults that have moved away from home and don't know what to cook (*put the pot noodles down*) and even for older adults that are looking to branch out and find new weeknight favourites.

   - This web application will be built using [Python](https://www.python.org/), [Flask](https://flask.palletsprojects.com/en/2.0.x/), [MongoDB](https://www.mongodb.com/), and a frontend framework called [Materialize](https://materializecss.com/).  
   - It  will allow users to store and easily access recipes via CRUD calls to a Mongo database.
   - This will be done in the context of a Flask application with HTML based user interfaces.


## Features

### Existing Features

- Responsive web application
- Functionality to allow users to create a login and sign in.
- CRUD functionality to allow users to view, add, edit and delete recipes.
- Search recipes functionality.

### Features to Implement

- CRUD functionality to allow admin users to edit categories, cuisines and cooking methods in the app rahter than through MongoDB. 
- Functionality to allow users to favourite recipes.
- Functionality to allow users to rate a recipe.
- Functionality to allow comments on recipes.
- Manage account functionality that will allow users to edit their username, password and delete their account.
- Functionality to allow users to upload a photo directly through the add_recipe/edit_recipe forms rather than linking to a photos URL.

When designing my web app I originally planned to have CRUD functionality for admin users as part of the MVP. During development I moved this to features to impliment to allow for more time to ensure existing features all work correctly without erros and provide visual responses to the user.

## Technologies used

In addition to the technologies mentioned throughout my ReadMe I used the following Technologies:
- HTML 5
- CSS 3
- Python 3
- Jinja 
- click==8.0.1
- dnspython==2.1.0
- Flask==2.0.1
- Flask-PyMongo==2.3.0
- itsdangerous==2.0.1
- pymongo==3.12.0
- Werkzeug==2.0.1
- To add my categories and cuisines into their respective collections I logged into the MongoShell and used `db.collections.insertMany()`.

## Testing

I have been testing my app throughout development as each feature is added and logging any errors/issues in the [issues](https://github.com/Tiff-C/ms3-backend-development/issues) tab of my repository with the tag of `bug`. I have also be referencing to these issues in my commit messages so that the issues, details and fixes are available in one location.

- [HTML Validation](/documentation/testing/html-validation.png)
   The section without a heading is the section for my Flash Messages, no other errors/issues were found.

- [CSS Validation](/documentation/testing/css-validation.png)
   The only erros with the CSS across the app are from the Materialzie CSS, no other errors/issues found.

- Python Validation
   To ensure my code is PEP8 compliant I have been using a Python linter in my development environment. There are no current issues/ errors.

## Deployment

To prepare the app for deployment to [Heroku](https://www.heroku.com/) I have created a `requirements.txt` file and a `Procfile`. I did this using the following commands in the terminal:

```
pip3 freeze --local > requirements.txt
```
```
echo web: python app.py > Procfile
```

When deploying the app on Heroku I used the GitHub deployment method and put the key, value pairs from the `env.py` in settings > config vars e.g `IP` as the key and `0.0.0.0` as the value.

Once this info had been input into Heroku and the `requirements.txt` file and the `Prockfile` have been pushed to GitHub, I then went to deploy > enable automatic deployments and then selected 'deploy branch'.

This method of deployment allows the app to update whenever new code is pushed to the GitHub repository.

### How to run This Project Locally

#### The `env.py` doc

To run the flask app locally you need to set up the environment defaults, as the setup contains sensitive info `env.py` has been added to `.gitignore`. An example of the code can be seen below with the sensitive data removed. 

*note: when the `DEBUG` variable is set to `False` you won't see exact error messages. When running the app to view live changes to the code set this variable to `True`.*

```python
import os

os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("SECRET_KEY", "<YOUR_SECRET_KEY_HERE>")
os.environ.setdefault("MONGO_URI", "<YOUR_MONGOU_URI_HERE>")
os.environ.setdefault("MONGO_DBNAME", "<YOUR_DBNAME_HERE>")
os.environ.setdefault("DEBUG", "False")
```

#### Installing required packages

To install the required Python packages run `pip install -r requirements.txt` in the command line.

#### Running the project locally

Run `flask run` in the command line.

## Credits



### Content

- My list of cooking methods came from [Studential](https://www.studential.com/university/student-cooking/cooking-methods) with the addition of "microwaving", "slowcooker", "no cook" and "other".

### Media

The images used in this project are all from BBC Good Food as this ensured all images were of the same size, quality and of a low file size. The specific pages where the images were found can be seen below.

To generate image links that would not be deleted over time I uploaded the images to [imgbb](https://imgbb.com/).

   - Categories
      - [Beef](https://images.immediate.co.uk/production/volatile/sites/30/2020/08/roast-beef-recipes-536cd86.jpg?quality=90&webp=true&resize=300,272)
      - [Breakfast](https://images.immediate.co.uk/production/volatile/sites/30/2020/08/healthy-fc28587.jpg?quality=90&webp=true&resize=300,272)
      - [Chicken](https://images.immediate.co.uk/production/volatile/sites/30/2021/04/Creamy-chicken-stew-32a0b1a.jpg?quality=90&webp=true&resize=300,272)
      - [Dessert](https://images.immediate.co.uk/production/volatile/sites/30/2020/08/plum-apple-cobbler-846b9e6.jpg?quality=90&resize=360,327)
      - [Lamb](https://images.immediate.co.uk/production/volatile/sites/30/2020/08/one-pan-easter-lamb-af14df4.jpg?quality=90&webp=true&resize=300,272)
      - [Misc](https://images.immediate.co.uk/production/volatile/sites/30/2021/09/Pumpkin-pickle-27aec22.jpg?quality=90&resize=360,327)
      - [Pasta](https://images.immediate.co.uk/production/volatile/sites/30/2021/05/tuna-pasta-salad-2-f1ae60f.jpg?quality=90&resize=360,327)
      - [Pork](https://images.immediate.co.uk/production/volatile/sites/30/2020/08/pork-belly-slices-14bc50f.jpg?quality=90&resize=360,327)
      - [Seafood](https://images.immediate.co.uk/production/volatile/sites/30/2020/08/creamy-salmon-leek-potato-traybake-367b3ff.jpg?quality=90&resize=360,327)
      - [Side](https://images.immediate.co.uk/production/volatile/sites/30/2020/08/salt-and-pepper-chips-fe15bf5.jpg?quality=90&resize=360,327)
      - [Vegan](https://images.immediate.co.uk/production/volatile/sites/30/2020/08/hdp-jambalaya-440-400-f14ba7f.jpg?quality=90&resize=360,327)
      - [Vegetarian](https://images.immediate.co.uk/production/volatile/sites/30/2020/08/slow-cooked-marrow-with-fennel-tomato_1-812f3fe.jpg?quality=90&resize=360,327)
  
### Code

- The regular expression for allowing spaces between words as well as apostrophe's in add_recipe.html inputs were taken from the following Stack Overflow post's: [allow spaces](https://stackoverflow.com/questions/15472764/regular-expression-to-allow-spaces-between-words) and [allow apostrophe's](https://stackoverflow.com/questions/5676541/regex-to-enforce-alpha-numeric-but-allow-apostrophes-and-hyphens).
- To dynamically add / remove input fields in add_recipe.html I used the code provided in this [Shouts.Dev post](https://shouts.dev/add-or-remove-input-fields-dynamically-using-jquery) as a starting point for my code.

### Acknowledgments

- I used the information provided in [Tubik's](https://tubikstudio.com/) [Case Study: Recipes App UX Design](https://blog.tubikstudio.com/case-study-recipes-app-ux-design/) as a starting point for ideas on the type of user and site owner goals for my project.