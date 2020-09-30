# FoodFuse

FoodFuse is an app created with Django, Python, and Selenium. The intent of the app is to save money and time, especially during times of a pandemic.

We all know the frustration of trying to find which app delivers our favorite restaurant/food. We also know the frustration of trying to find which app has the cheapest delivery fees and shortest delivery times. FoodFuse solves all of that. 

FoodFuse searches and sorts through the 4 major food delivery apps Doordash, Uber Eats, Postmates, and Grubhub by the user's location and returns the data. FoodFuse will provide the users with a comparison of the delivery fee's and delivery times between each service so that the user can make an educated choice on which app to use.

Fun fact: FoodFuse utilizes the Pantone 2020 color of the year, Classic Blue. 😁🔷

<!-- example images
![Imgur Image](https://i.imgur.com/pb3hvSv.jpg) -->

## Team
---
* [Cristina Nguyen](https://github.com/crnguyen)
* [Tanner Leigh](https://github.com/thleigh)

## Deployed Site
---
* [FoodFuse]()

## User Stories / Features
---
* Every user will be able to signup and keep a personalized account in order to speed up the search process and store data of their favorite restarants.

* Users will be able to access the Doordash, Uber Eats, Postmates, and Grubhub, data and app, all in one location.

* User's will be able to search for their favorite restaurants and/or the types of food that they are craving.

## Technologies
---
* [Django](https://www.djangoproject.com/)
* [Python](https://www.python.org/)
* [Selenium](https://www.selenium.dev/)
* [Bootstrap](https://getbootstrap.com/)

## ERD
---
## Wireframe
---
* [Wireframe](https://whimsical.com/8ZG1we7qiPufc8D7ZoJwhb)

## Installation
---

## Models
---
### User Model

| Column name   | Data Type     |  
| ------------- | ------------- | 
| id            |               |                                             
| location      | CharField     |                    
| restaurant    | CharField     |      
| delivery_fee  | CharField     | 
| delivery_time | CharField     | 
| rating        | CharField     | 

### Restaurant Model

| Column name   | Data Type     |  
| ------------- | ------------- | 
| id            |               |                                             
| username      | CharField     |                    
| password      | CharField     |      
| location      | CharField     | 
| restaurants   | CharField - ManyToMany | 

## Routes
---
<!-- | Routes        | Route Methods Used    | Notes                                             | 
| ------------- | ----------------------| ----------------------------------                | 
| auth.js       | GET, POST             | controls signup/login and auth of user            |
| comments.js   | POST                  | create comment data on details page               |
| favorites.js  | GET, POST, PUT, DELETE| favorite, delete a recipe, update recipe's title  |
| user.js       | GET, PUT, DELETE      | account info page, user can update their email    | -->

## Sprints
---
### 0 - Planning

### 1 - Data Parsing/Setting Up Views

### 2 - Storing Data in Database / CRUD

### 3 - UX/UI Design / CSS

### 4 - Add Finishing Touches

## Code Snippets
---

## Conclusion
---