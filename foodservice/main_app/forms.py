from django import forms

class TestForm(forms.Form):
    location = forms.CharField()
    restaurant = forms.CharField()