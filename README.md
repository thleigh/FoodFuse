# FoodFuse

FoodFuse is an app created with Django, Python, and Selenium. The intent of the app is to save money and time, especially during times of a pandemic.

We all know the frustration of trying to find which app delivers our favorite restaurant/food. We also know the frustration of trying to find which app has the cheapest delivery fees and shortest delivery times. FoodFuse solves all of that. 

FoodFuse searches and sorts through the 4 major food delivery apps Doordash, Uber Eats, Postmates, and Grubhub by the user's location and returns the data. FoodFuse will provide the users with a comparison of the delivery fee's and delivery times between each service so that the user can make an educated choice on which app to use.

Fun fact: FoodFuse utilizes the Pantone 2020 color of the year, Classic Blue. 🔷

## Deployed Site
---
* ### [FoodFuse](https://foodfuse.herokuapp.com/)

#### Image Previews
---
#### Homepage
![Imgur](https://i.imgur.com/4wh21ba.jpg)

#### Data Page - after typing in location
![Imgur](https://i.imgur.com/UH0ll9u.jpg)

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

## Other Resources
---
* [Linear Gradients](https://www.eggradients.com/)

## ERD
---
## Wireframe
---
* [Wireframe](https://whimsical.com/8ZG1we7qiPufc8D7ZoJwhb)

## Installation
---
In order to run our app locally, you will need to fork and clone this repo.

Once a local repo is made, run ```npm i``` in the project file's terminal.

You will need the chromedriver version that is compatible with your version of Google Chrome. This can be found [here](https://chromedriver.chromium.org/). 
 - put it somewhere that you know the path to.

 Next, you will need to create a ```chrome_driver.py``` file and add that to your ```.gitignore```. 

 Inside of ```chrome_driver.py```, create a variable called ```chrome_location``` and set that equal to the path of the chromedriver.

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

![Imgur](https://i.imgur.com/tAteTmo.jpg)

### User Model - used Django's built in auth model

![Imgur](https://i.imgur.com/l3C7jNj.jpg)

## Sprints
---
### 0 - Planning
We spent the first three days setting up our idea, ERD, wireframe, and general layout. ERD/wireframe is linked above. 

### 1 - Data Parsing/Setting Up Views
For the views, we wanted to keep this portion simple. Working with views was pretty straight forward and consisted of setting up our pages, urls, and what we wanted for our contents of each page.

### 2 - Storing Data in Database / CRUD
This part took about 70% of our time to do because it was dependent on the data being pulled from Selenium. It seemed like the data on the food service sites was constantly changing, so we had to make sure that we were able to pull data from the sites daily. We also implemented any error handling for cases like this. For the Restaurants model, we included the CRUD route. The Create and Delete routes are working perfectly on the backend, however, one thing we need to implement is the update route. We were having so many issues with model creation and we were able to post and delete on the backend using Ajax and jQuery, but the update view was complicated to understand. 

### 3 - UX/UI Design / CSS
We utilized Bootstrap 4 and CSS for our layout and effects. Also included Pantone Color of the Year, just because.

### 4 - Add Finishing Touches
We spent our time sprucing up the layout and making our app look less plain. We also added in Bootstrap carousel to the About Us page and added in the fade effect to the existing carousel on the Index page. 

## Code Snippets
---
### Model, CRUD, and posting to the backend

Adding doordash to favorites page through a button click. Implemented Ajax and jQuery and provided a unique identifier for food service data on the HTML portion. Then in views.py, the data was created and pushed to the backend. Below is an example of the doordash data, and it's the same process for UberEats and Postmates.

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

### Selenium execution
This was our bread and butter. In our index function, we asynchronously ran our scraper_function that called all 3 of the selenium bots while passing in data that was submitted by the user. 

```python
## INDEX VIEW ##
def index(request):
    # Checks if the request is a POST 
    if request.method == "POST" and 'reset' in request.POST:
        dd_quit()
        ue_quit()
        pm_quit()
        print('quit')
        # Will populate our form with what the user submits
        # If what the user inputs works
    else:
        form = SearchForm(request.POST)
        if form.is_valid():
            # Gets the data in a clean format
            location = form.cleaned_data['location']
            # passes the location data to the next view
            request.session['location'] = location
            # Runs the functions asynchronously
            asyncio.run(scraper_function(request))
            return HttpResponseRedirect('/data/')

    form = SearchForm()
    return render(request, 'index.html', 
        {
        'form': form, 
        })

async def scraper_function(request):
    # accepts the location from the index view
    location = request.session.get('location')
    task1 = asyncio.ensure_future(doordash(location))
    task2 = asyncio.ensure_future(postmates(location))
    task3 = asyncio.ensure_future(ubereats(location))
    await asyncio.wait([
        task1, task2, task3
    ])
```

## Conclusion
---
In conclusion, working with Django and Selenium was very challenging. They were both technologies we had to learn and use for the first time while creating this app but ultimately
provided a good foundation for flexible coding. Through this process we had to learn fast and utilize the documents and resources that were provided online. Google, stackoverflow, and Youtube definitely became our bestfriends during this process. Anything can be learned or solved through the power of search. 

Looking back, Selenium would probably not be the best thing to use for an app. Big companies change the way they display their data almost every day making it very difficult
to consistently post data without having to stay on your feet. 
