# NomNoms

## Table of Contents

   1. [UX](#ux)
      - [Project Goals](#project-goals)
      - [User Goals](#user-goals)
      - [Owner Goals](#owner-goals)
      - [User Stories](#user-stories)
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

   - This web application will be built using [Python](https://www.python.org/), [Flask](https://flask.palletsprojects.com/en/2.0.x/), [MongoDB](https://www.mongodb.com/), and a frontend framework called [Materialize](https://materializecss.com/).  
   - It  will allow users to store and easily access recipies via CRUD calls to a Mongo database.
   - This will be done in the context of a Flask application with HTML based user interfaces.

### User Goals

- __External Users Goal__: Find and share recipies.

### Developer and Business Goals

- __Site Owner's Goal__: The site owner is looking for a place to find and share recipes as well as      wanting to build a database of recipies for their business needs.

### User Stories

(will fill section as project progresses)

### Design Choices

(will fill section as project progresses)

#### Database Schema

When thinking about my databases structure I decided to see if I could find any example recipie database's. During my search I found [schema.org/Recipe](https://schema.org/Recipe) and the specific [Schema](https://developers.google.com/search/docs/advanced/structured-data/recipe) Google use for their recipies database. Using these and [The Meal DB](https://www.themealdb.com/) for catagories and cuisine lists. I decided on the following structure for my database.

__Collections:__ 
1. Users

   The user authentication for this project will reuse the code from the [Mini Project Walkthrough](https://github.com/Tiff-C/task-master) with the addition of `superusers` to authenticate admin users instead of `if username.lower() == 'admin'`.

   ```JSON
   {
      "username": "username",
      "password": "password"
   }
   ```

2. Categories

   The categories list has been taken from [The Meal DB | Categories](https://www.themealdb.com/api/json/v1/1/list.php?c=list). The categories will be available for users to select when inputting a recipe. I have decided to use the specified categories instead of user input to avoid the creation of duplicate categories through typo errors, naming variations etc. The complete list of categories can be seen in [data.json](data.json). Adding and removing categories will require `username['superuser'] == True`.

   ```JSON
   {
      "recipeCategory": "category"
   }
   ```

3. Cuisines

   The cuisines list has been taken from [The Meal DB | Cuisines](www.themealdb.com/api/json/v1/1/list.php?a=list). The cuisines will be available for users to select when inputting a recipe. I have decided to use the specified cuisines instead of user input to avoid the creation of duplicate categories through typo errors, naming variations etc. The complete list of cuisines can be seen in [data.json](data.json) Adding and removing categories will require `username['superuser'] == True`.

   ```JSON
   {
      "recipeCuisine": "cuisine"
   }
   ```

4. Recipes

   For my recipies collection I will be using a condensed version of the [Recipes Schema](https://schema.org/Recipe) from [Schema.org](https://schema.org/). An example of this and the expected data types can be seen below. 
   This format along with the flexibility providided by using a non-relational database like MongoDB will allow users to add their own units and measurements based on preference. I could add all units and measurements that users can then select as I have for Categories however due to the large variation of units and measurements used in recipies (e.g 'a pinch of salt', 'a slice of bread', 'half a pack of biscuits')I have decided that for now it would be best to let users input this themselves. This is something I may look at in the future to bring a little more uniformity to my data however I feel this is not required for my milestone project.

   ```JSON
   {
      "name": "text",
      "prepTime": "duration",
      "cookTime": "duration",
      "cookingMethod": "text",
      "recipeCategory": "text",
      "recipeCuisine": "text",
      "recipeIngredient": ["item list"],
      "recipeInstructions": ["item list"],
      "recipeYield": "quantative value",
      "recipeImage": "url"
   }
   ```


### Wireframes

(will fill section as project progresses)

## Features

### Existing Features

(will fill section as project progresses)

### Features to Implement

(will fill section as project progresses)

## Technologies used

(will fill section as project progresses)

## Testing

(will fill section as project progresses)

## Deployment

(will fill section as project progresses)

### How to run This Project Locally

