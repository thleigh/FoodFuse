from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SearchForm(forms.Form):
    location = forms.CharField(label='Please enter a city or zipcode to get started', max_length=300, widget=forms.TextInput(attrs={'style': 'height: 30px'}))
    
class RestaurantForm(forms.Form):
    restaurant = forms.CharField()

class FavoriteForm(forms.Form):
    favorites = forms.CharField()