### User Goals

#### First Time User Goals 
   - __As a first time user I want to:__
      - be able to navigate around the site and find the content I am looking for with ease.
      - filter and / or search for specific recipes
      - browse for inspiration for meals

#### Returning User Goals
   - __As a returning user I want to:__
      - be able to save my favourite recipes
      - be able to share my recipes with friends
      - share my recipes with others
      - edit or delete the recipes I have shared
      - see seasonal recipe suggestions
      - see recommended recipes based on my saved or viewed recipes
      - leave recipe reviews / ratings 
      - get email updates about new recipes I may like or Seasonal inspiration

### Developer and Business Goals / Stories

   - __As the site owner I want to:__ 
      - create a place to find and share authentic home made dinner ideas
      - build a database of homemade recipes from around the world
      - view statistics on recipe interactions and frequent user habits
      - add new categories and cusines as my database grows


### Design Choices

#### App Layout

As there as a vast range of intended users for this site the layout must feel really simple, other than the recipe pages themselves the main layout will be square cards with images set as backgrounds with the card title below to ensure the text is easily readable. Originally I planned for the cards to scroll left and right across the screen with arrow buttons being provided for desktop users. This layout is currently widley used in apps and sites and can be found across all platforms including tv apps, shopping apps, food apps and many more. I felt the use of this layout would hopefully mean all users would know how to interact with the app upon first use. 
However during development and testing I realised this may not be suitible for my app as the categories list contains 24 items and the carousel felt overcrowded with even 10 or so items. I thought a solouting to this could be to add a show more button that takes the user to a page with all categories listed. This however would have creted another step between the user arriving on the page and being able to view the recipes in that category. With this in mind I decided to leave the cards in responsive rows.

#### Color Scheme

For the same reasons listed in the app layout section is want the colour scheme of my app to feel warm and welcoming whilst remaining easily readable. The specific colours used across my project are:
   - Materialize yellow darken-4 (#fbc02d)
   - Materialize yellow lighten-5 (#fffde7)

#### Typography

For the typography of the site I will be using Google fonts. The font used in my webb app is Yaldevi from the Sans-serif font family which has a high level of readability.

#### Imagery

As the main page of the site is mainly made up of images the images for this site need to be inviting and draw the user in. They will also need to be small file sizes to avoid longer loading times for users.

#### Database Schema

When thinking about my databases structure I decided to see if I could find any example recipie database's. During my search I found [schema.org/Recipe](https://schema.org/Recipe) and the specific [Schema](https://developers.google.com/search/docs/advanced/structured-data/recipe) Google use for their recipes database. Using these and [The Meal DB](https://www.themealdb.com/) for catagories and cuisine lists. I decided on the following structure for my database.

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

   For my recipes collection I will be using a condensed version of the [Recipes Schema](https://schema.org/Recipe) from [Schema.org](https://schema.org/). I have also changed the property names from camelCase to Snake Case to provide uniformity across the project. An example of this and the expected data types can be seen below. 
   This format along with the flexibility providided by using a non-relational database like MongoDB will allow users to add their own units and measurements based on preference. I could add all units and measurements that users can then select as I have for Categories however due to the large variation of units and measurements used in recipes (e.g 'a pinch of salt', 'a slice of bread', 'half a pack of biscuits')I have decided that for now it would be best to let users input this themselves. This is something I may look at in the future to bring a little more uniformity to my data however I feel this is not required for my milestone project.

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

Below are examples of the wireframes used for this project, as the web app has quite a few views that are similar to eachother and the focus of this project is on the data I haven't created an individual wireframe for each view.

- [Site Map](/documentation/wireframes/ms3-site-map.png)
- [Home](/documentation/wireframes/ms3-home.png)
- [Login](/documentation/wireframes/ms3-login.png)
