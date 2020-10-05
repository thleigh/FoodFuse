# FoodFuse

FoodFuse is an app created with Django, Python, and Selenium. The intent of the app is to save money and time, especially during times of a pandemic.

We all know the frustration of trying to find which app delivers our favorite restaurant/food. We also know the frustration of trying to find which app has the cheapest delivery fees and shortest delivery times. FoodFuse solves all of that. 

FoodFuse searches and sorts through the 4 major food delivery apps Doordash, Uber Eats, Postmates, and Grubhub by the user's location and returns the data. FoodFuse will provide the users with a comparison of the delivery fee's and delivery times between each service so that the user can make an educated choice on which app to use.

Fun fact: FoodFuse utilizes the Pantone 2020 color of the year, Classic Blue. 😁🔷

## Deployed Site
---
* ### [FoodFuse](https://foodfuse.herokuapp.com/)

#### Image Previews
---

#### Homepage
![Imgur](https://i.imgur.com/4wh21ba.jpg)

#### Data Page - after typing in location
![Imgur](https://i.imgur.com/PRUotld.jpg)


## Team
---
* [Cristina Nguyen](https://github.com/crnguyen)
* [Tanner Leigh](https://github.com/thleigh)

## User Stories / Features
---
* Every user will be able to signup and keep a personalized account in order to speed up the search process and store data of their favorite restarants.

* Users will be able to access the Doordash, Uber Eats, Postmates, and Grubhub, data and app, all in one location.

* User's will be able to search for their favorite restaurants and/or the types of food that they are craving.

## Technologies
---
* [Django](https://www.djangoproject.com/)
* [Python](https://www.python.org/)
* [jQuery](https://jquery.com/)
* [Ajax](https://api.jquery.com/category/ajax/)
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
### Restaurant Model

| Column name   | Data Type     |  
| ------------- | ------------- | 
| id            |               |                                             
| location      | CharField     |                    
| restaurant    | CharField     |      
| delivery_data  | CharField     | 
| user_id | CharField     | 

### User Model

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

Adding doordash to favorites page through a button click. Implemented Ajax and jQuery and provided a unique identifier for food service data on the HTML portion. Then in views.py, the data was created and pushed to the backend. Below is an example of the doordash data, but it's the same process for UberEats and Postmates.

```HTML
<div id="doordash-data">
      <h2>DOORDASH</h2>
      {% for doordash in doordash %}
      <div class="databox">
        <p>Restaurant: {{ doordash.restaurant_name }}</p>
        <p>Delivery Data: {{ doordash.delivery_cost }} · {{ doordash.delivery_time }}</p>
        <form id="{{doordash.restaurant_name}}{{doordash.delivery_cost}}{{doordash.delivery_time}}" action="/favorites/" method="POST">
          {% csrf_token %}
          <input type="hidden" id="{{doordash.restaurant_name}}{{doordash.delivery_cost}}{{doordash.delivery_time}}" value="{{doordash.restaurant_name}}" name="restaurant">
          <input type="hidden" value="{{doordash.delivery_cost}}" name="delivery_cost">
          <input type="hidden" value="{{doordash.delivery_time}}" name="delivery_time">
          <button type="button" value="{{doordash.restaurant_name}}{{doordash.delivery_cost}}{{doordash.delivery_time}}" class="btn btn-primary doordash-favorites">Add {{ doordash.restaurant_name }} to favorites</button>
        </form>
    </div> 
    {% endfor %}
</div>
```

```Javascript
// ajax call for doordash
  $(".doordash-favorites").on("click", function(evt){
    evt.preventDefault()
    const value = evt.target.value
    const formElements = $("#doordash-data form") 
    let data = null
    for (element of formElements){
      if (element.id === value)
        data = $(element).serializeArray()
    }
    if (data){
      let json = {}
      for (object of data){
        json[object.name] = object.value
      }
      data = json
    }
    // just to assign a user to a favorite
    data.id = 1
    if (!data.location){
      data.location = null
    }

    $.ajax({
      url: "/add_favorite/",
      method: "POST",
      dataType: "json",
      data: JSON.stringify(data)
    }).done(function(data){
      window.location.replace("/favorites/")
    })
  })
```

```Python
## CREATE VIEW ##
@csrf_exempt
def add_favorite(request):
    if request.method == "POST":
        data = json.load(request)
        # print("REQUEST OBJECT:", data)
        # print("PRINTING DATA:",data)
        if "delivery_data" not in data:
            data["delivery_data"] = data["delivery_cost"] + " " + data["delivery_time"]
        user = User.objects.get(id=data['id'])
        restaurant = dict(
            user=user,
            location=data['location'],
            restaurant=data['restaurant'],
            delivery_data=data['delivery_data']
        )
        new_restaurant = Restaurant.objects.create(**restaurant)
        return JsonResponse(True, status=200, safe=False)
```

## Conclusion
---