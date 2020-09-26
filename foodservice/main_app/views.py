from django.shortcuts import render, redirect
# from .models import Cat, CatToy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

# DEFAULT
def about(request):
    return render(request, 'about.html')

def index(request):
  return render(request, 'index.html')
