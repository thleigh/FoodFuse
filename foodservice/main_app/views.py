from django.shortcuts import render, redirect
from .models import Restaurant, User, Test
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .doordash import doordash, final_list
from .forms import SearchForm
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
                    return HttpResponseRedirect('/user/'+u)
                else:
                    print('The account has been disabled.')
        else:
            print('The username and/or password is incorrect.')
    else: # it was a GET request so send the empty login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

##trying to add email to login form
class EmailLoginForm(AuthenticationForm):
    def clean(self):
        try:
            self.cleaned_data["username"] = get_user_model().objects.get(email=self.data["username"])
        except ObjectDoesNotExist:
            self.cleaned_data["username"] = "a_username_that_do_not_exists_anywhere_in_the_site"
        return super(EmailLoginForm, self).clean()

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/user/'+str(user))
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

# def index(request):
#   return render(request, 'index.html')

# class Test(CreateView):
#     model = Test
#     fields = '__all__'
#     success_url = '/test'


def index(request):

    # Checks if the request is a POST 
    if request.method == "POST":
        # Will populate our form with what the user submits
        form = SearchForm(request.POST)
        # If what the user inputs works
        if form.is_valid():
            # Gets the data in a clean format
            location = form.cleaned_data['location']
            # restaurant = form.cleaned_data['restaurant']

            # print(location)
            doordash(location)
            # print(final_list)

    form = SearchForm()
    return render(request, 'index.html', {'form': form, 'data': final_list})

# def datapage(request):
#     print(final_list)
#     return render(request, 'data.html', {'data': final_list})

#   class CatToyCreate(CreateView):
#     model = CatToy
#     fields = '__all__'
#     success_url = '/cattoys'

class RestaurantCreate(CreateView):
    model = Restaurant
    fields = '__all__'
    success_url = '/restaurants/'

# class UserCreate(CreateView):
