## Project Proposal

### How About A Drink Search App

**Goal**
The goal of this project is to provide a user friendly application that allows users to search for and save cocktail recipes. And maybe have a couple along the way.

**Expected Users**
The application will be useful for experienced mixologists and amatuers alike. Bartenders and mixologists could use this application to look up a drink request they don't know, while beginners can look up what types of drinks they could make at home with ingredients they have at the house.

**Data**
The data resource used for this site will be TheCoccktailDB API. This API holds over 1000 cocktail recipes. You can also query spirits, ingredients, and even glass types.

**Outline**
The data schema will consist of a users table, a favorites table, and a follows table. With the possible addition of a cocktail table down the line, for users to create their own cocktails. Example queries include:

* Search for cocktail name (Rum Runner)
* Search for ingredient name (Pineapple Juice)
* Search for spirit (Gin)
* Search by cocktail names by letter (A)

Also, the site will include additional user functionality, including creating, updating, and deleting accounts, with which the user can save, edit, and delete favorites. Therefore, user tables will be created in the database along with a favorites table. Issues aligning all of these database relationships are certainly expected. Each user will have unique login usernames and encrypted password authentication. Additional functionality could include filtering search functionality as well as allowing users to create their own cocktails to share with the community.

