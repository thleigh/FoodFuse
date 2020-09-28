from django import forms

class SearchForm(forms.Form):
    location = forms.CharField()
    # restaurant = forms.CharField()