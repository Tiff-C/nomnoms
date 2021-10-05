# NomNoms 

> "Cooking made simple"

## Table of Contents

   1. [UX](#ux)
      - [Project Goals](#project-goals)
      - [User Goals](#user-goals)
      - [Owner Goals](#owner-goals)
      - [Design Choices](#design-choices)
         - [Database Schema](#database-schema)
      - [Wireframes](#wireframes)
   2. [Features](#features)
      - [Existing Features](#existing-features)
      - [Features to implement](#features-to-impliment)
   3. [Technologies Used](#technologies-used)
   4. [Testing](#testing)
   5. [Deployment](#deployment)
      - [How to run this project locally](#how-to-run-this-project-locally)
   6. [Credits](#credits)
      - [Content](#content)
      - [Media](#media)
      - [Code](#code)
      - [Acknowledgments](#acknowledgements)

## UX

### Project Goals

   This project is my third Milestone Project, the purpose of this project is to demonstrate the skills and knowledge I have developed during the Python Essentials and Backend Development modules. I have chosen project idea 1 - create an online cookbook.

   This cookbook will be a collection of simple homemade recipes initially from myself but hopefully in time they will be from around the world. It will be targeted at people who are looking for easy meal ideas that taste great! 
   Large recipe databases such as [BBC Good Food]() or [The Food Network]() are full of things you might want to try for your next dinner party but not too many things you can whip up in 30 mins using basic cupboard supplies or even using food from the freezer. Nothing fancy just simple food that tastes good.
   The intended users of the app range from parents looking for meal ideas for their weekly shop, young adults that have moved away from home and don't know what to cook (*put the pot noodles down*) and even for older adults that are looking to branch out and find new weeknight favourites.

   - This web application will be built using [Python](https://www.python.org/), [Flask](https://flask.palletsprojects.com/en/2.0.x/), [MongoDB](https://www.mongodb.com/), and a frontend framework called [Materialize](https://materializecss.com/).  
   - It  will allow users to store and easily access recipies via CRUD calls to a Mongo database.
   - This will be done in the context of a Flask application with HTML based user interfaces.

### User Goals

#### First Time User Goals 
   - __As a first time user I want to:__
      - be able to navigate around the site and find the content I am looking for with ease.
      - filter and / or search for specific recipies
      - browse for inspiration for meals

#### Returning User Goals
   - __As a returning user I want to:__
      - be able to save my favourite recipes
      - be able to share my recipes with friends
      - share my recipes with others
      - edit or delete the recipes I have shared
      - see seasonal recipe suggestions
      - see reccomended recipes based on my saved or viewed recipes
      - leave recipe reviews / ratings 
      - get email updates about new recipes I may like or Seasonal inspiration

### Developer and Business Goals / Stories

   - __As the site owner I want to:__ 
      - create a place to find and share authentic home made dinner ideas
      - build a database of homemade recipies from around the world
      - view statistics on recipe interactions and frequent user habits
      - add new categories and cusines as my database grows


### Design Choices

#### App Layout

As there as a vast range of intended users for this site the layout must feel really simple, other than the recipe pages themselves the main layout will be square cards with images set as backgrounds with the card title below to ensure the text is easily readable. The cards will scroll left and right across the screen with arrow buttons being provided for desktop users. This layout is currently widley used in apps and sites and can be found across all platforms including tv apps, shopping apps, food apps and many more. The use of this layout will hopefully mean all users will know how to interact with the app upon first use.

#### Color Scheme

For the same reasons listed in the app layout section is want the colour scheme of my app to feel warm and welcoming whilst remaining easily readable. The specific colours used across my project are:
   - Materialize yellow darken-4 (#fbc02d)
   - Materialize yellow lighten-5 (#fffde7)

#### Typography

For the typography of the site I will be using Google fonts, the font from the Sans-serif font family which has a high level of readability.

#### Imagery

As the main page of the site is mainly made up of images the images for this site need to be inviting and draw the user in. They will also need to be small file sizes to avoid longer loading times for users.

#### Database Schema

When thinking about my databases structure I decided to see if I could find any example recipie database's. During my search I found [schema.org/Recipe](https://schema.org/Recipe) and the specific [Schema](https://developers.google.com/search/docs/advanced/structured-data/recipe) Google use for their recipies database. Using these and [The Meal DB](https://www.themealdb.com/) for catagories and cuisine lists. I decided on the following structure for my database.

__Collections:__ 
1. Users

   The user authentication for this project will reuse the code from the [Mini Project Walkthrough](https://github.com/Tiff-C/task-master) with the addition of `superusers` to authenticate admin users instead of `if username.lower() == 'admin'`.

   ```JSON
   {
      "username": "username",
      "password": "password",
      "superuser": "boolean",
      "user_recipes": ["list of recipe IDs"],
      "user_favourites": ["list of recipe IDs"]
   }
   ```

2. Categories

   The categories list has been taken from [The Meal DB | Categories](https://www.themealdb.com/api/json/v1/1/list.php?c=list) with 'starters' removed as I felt this was less relevant to my site. The categories will be available for users to select when inputting a recipe. I have decided to use the specified categories instead of user input to avoid the creation of duplicate categories through typo errors, naming variations etc. The complete list of categories can be seen in [data.json](data.json). Adding and removing categories will require `username['superuser'] == True`.

   ```JSON
   {
      "recipe_category": "category",
      "category_image": "link"
   }
   ```

3. Cuisines

   The cuisines list has been taken from [The Meal DB | Cuisines](www.themealdb.com/api/json/v1/1/list.php?a=list). The cuisines will be available for users to select when inputting a recipe. I have decided to use the specified cuisines instead of user input to avoid the creation of duplicate categories through typo errors, naming variations etc. The complete list of cuisines can be seen in [data.json](data.json) Adding and removing categories will require `username['superuser'] == True`.

   ```JSON
   {
      "recipe_cuisine": "cuisine"
   }
   ```

4. Cooking Methods

   The list of cooking methods came from [Studential](https://www.studential.com/university/student-cooking/cooking-methods) with the addition of "microwaving", "slowcooker", "no cook" and "other". The cooking methods will be available for users to select when inputting a recipe, they will have the option of selecting multiple methods as some recipes may require mmore than one cooking method. I decided to use the specified cooking methods instead of user input to avoid the creation of duplicate categories through typo errors, naming variations etc. The complete list of cooking methods can be seen in [data.json](data.json) Adding and removing categories will require `username['superuser'] == True`.

      ```JSON
   {
      "cooking_method": "cooking_method"
   }
   ```

5. Recipes

   For my recipies collection I will be using a condensed version of the [Recipes Schema](https://schema.org/Recipe) from [Schema.org](https://schema.org/). I have also changed the property names from camelCase to Snake Case to provide uniformity across the project. An example of this and the expected data types can be seen below. 
   This format along with the flexibility providided by using a non-relational database like MongoDB will allow users to add their own units and measurements based on preference. I could add all units and measurements that users can then select as I have for Categories however due to the large variation of units and measurements used in recipies (e.g 'a pinch of salt', 'a slice of bread', 'half a pack of biscuits')I have decided that for now it would be best to let users input this themselves. This is something I may look at in the future to bring a little more uniformity to my data however I feel this is not required for my milestone project.

   ```JSON
   {
      "name": "text",
      "author": "username",
      "created_date": "date / time",
      "prep_time": "duration",
      "cook_time": "duration",
      "cooking_method": "text",
      "recipe_category": "text",
      "recipe_cuisine": "text",
      "recipe_ingredient": ["item list"],
      "recipe_instructions": ["item list"],
      "recipe_yield": "quantative value",
      "recipe_image": "url",
      "interaction_statistic": [
         {
            "type": "comments_counter",
            "comments": [],
            "comments_count": [],
         },
         {
            "type": "favourites_counter",
            "favourites_count": [],
         }
      ]
   }
   ```


### Wireframes

- [Site Map](/documentation/wireframes/ms3-site-map.png)
- [Home](/documentation/wireframes/ms3-home.png)

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

## Technologies used

To add my categories and cuisines into their respective collections I logged into the MongoShell and used `db.collections.insertMany()`.

## Testing

I have been testing my app throughout development and logging any errors/issues in the [issues](https://github.com/Tiff-C/ms3-backend-development/issues) tab of my repository with the tag of `bug`. I have also be referencing to these issues in my commit messages so that the issues, details and fixes are available in one location.

## Deployment

To prepare the app for deployment to Heroku I have created a `requirements.txt` file and a `Prockfile`. I did this using the following commands in the terminal:

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

- I used the information provided in [Tubik's](https://tubikstudio.com/) [Case Study: Recipies App UX Design](https://blog.tubikstudio.com/case-study-recipes-app-ux-design/) as a starting point for ideas on the type of user and site owner goals for my project.