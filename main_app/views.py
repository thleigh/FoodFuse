from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from .models import Restaurant, Users
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from asgiref.sync import sync_to_async
from django.template import RequestContext
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User

# from .scraper import scraper_function, 
from .doordash import doordash, doordash_unparsed_list, doordash_data, doordash_restaurant_data, doordashRestaurant, doordash_data_specific
from .postmates import postmates, postmates_unparsed_list, postmates_data, postmates_restaurant_data, postmatesRestaurant, postmates_data_specific
from .ubereats import ubereats, ubereats_unparsed_list, ubereats_data, ubereats_restaurant_data, ubereatsRestaurant, ubereats_data_specific
import asyncio, time
from .forms import SearchForm, RestaurantForm, FavoriteForm

# Create your views here.

# LOGIN
def login_view(request):
    if request.method == 'POST':
        # try to log the user in
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user) # log the user in by creating a session
                    # return HttpResponseRedirect('/')
                    return HttpResponseRedirect('/user/'+u+'/')
                else:
                    print('The account has been disabled.')
        else:
            print('The username and/or password is incorrect.')
    else: # it was a GET request so send the empty login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/user/'+str(user)+'/')
        else:
            return HttpResponse('<h1>Try Again</h1>')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

#PROFILE
@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    # cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username })

# DEFAULT
def about(request):
    return render(request, 'about.html')

def index(request):
    # Checks if the request is a POST 
    if request.method == "POST":
        # Will populate our form with what the user submits
        form = SearchForm(request.POST)
        # If what the user inputs works
        if form.is_valid():
            # Gets the data in a clean format
            location = form.cleaned_data['location']
            request.session['location'] = location
            asyncio.run(scraper_function(request))
            return HttpResponseRedirect('/data/')
    form = SearchForm()
    return render(request, 'index.html', 
        {
        'form': form, 
        })

async def scraper_function(request):
    location = request.session.get('location')
    # print(location)
    task1 = asyncio.ensure_future(doordash(location))
    task2 = asyncio.ensure_future(postmates(location))
    task3 = asyncio.ensure_future(ubereats(location))
    await asyncio.wait([
        task1, task2, task3
    ])

def data(request):
    final_dd_data = []
    final_pm_data = []
    final_ue_data = []
    for dd_data in doordash_unparsed_list:
        doordash_data(dd_data)
        final_dd_data.append(doordash_data.results)

    postmates_fixed_list = list(filter(None, postmates_unparsed_list))
    for pm_data in postmates_fixed_list:
        postmates_data(pm_data)
        final_pm_data.append(postmates_data.results)

    for ue_data in ubereats_unparsed_list:
        ubereats_data(ue_data)
        final_ue_data.append(ubereats_data.results)
    # print(ubereats_unparsed_list)

    if request.method == "POST":
        # Will populate our form with what the user submits
        form = RestaurantForm(request.POST)
        # If what the user inputs works
        if form.is_valid():
            # Gets the data in a clean format
            restaurant = form.cleaned_data['restaurant']
            request.session['restaurant'] = restaurant
            return HttpResponseRedirect('/restaurant/')

    form = RestaurantForm()
    return render(request, 'data.html', {
        'doordash': final_dd_data, 
        'postmates': final_pm_data,
        'ubereats': final_ue_data,
        'form': form,
    })

def restaurant(request):
    restaurant = request.session.get('restaurant')
    postmatesRestaurant(restaurant)
    doordashRestaurant(restaurant)
    ubereatsRestaurant(restaurant)
    print(postmates_restaurant_data)
    print(doordash_restaurant_data)
    print(ubereats_restaurant_data)
    for pm_restaurant in postmates_restaurant_data:
        postmates_data_specific(pm_restaurant)
        # postmates_data_specific.results
    for dd_restaurant in doordash_restaurant_data:
        doordash_data_specific(dd_restaurant)
        # doordash_data_specific.results
    for ue_restaurant in ubereats_restaurant_data:
        ubereats_data_specific(ue_restaurant)
    return render(request, 'restaurant.html', {
        'pm': postmates_data_specific.results,
        'dd': doordash_data_specific.results,
        'ue': ubereats_data_specific.results,
    })

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
        new_restaurant = Restaurant.objects.create(**restaurant) ####CREATE - creating an instance in the restaurant model
        return JsonResponse(True, status=200, safe=False)

## DELETE VIEW ##
@csrf_exempt
def remove_favorite(request):
    if request.method == "POST":
        data = json.load(request)
        user_id = data["user_id"]
        id=data["id"]
        Restaurant.objects.filter(id=id, user=user_id).delete()
        return JsonResponse(True, status=200, safe=False)

@csrf_exempt
def favorites_show(request):
    # print("querying restaurant:")
    restaurants = Restaurant.objects.all()
    # print("restaurants:",restaurants)
    restaurants = [restaurant.__dict__ for restaurant in restaurants]
    # print(restaurants)
    return render(request, 'Favorites/favorites.html', {'restaurants': restaurants})

## UPDATE VIEW ##

# class UpdateFavorite(UpdateView):
#     model = Restaurant
#     fields = ['location', 'restaurant', 'delivery_data', 'user_id']

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.save()
#         return HttpResponseRedirect('/favorites/')


# # ####404 error page ???
# def error_404(request):
#         data = {}
#         return render(request,'404.html', data)

# def error_404_view(request, exception):
#     return render(request, 'main_app/404.html')

# def error_500_view(request, exception):
#     return render(request, 'main_app/500.html')