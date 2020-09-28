from django.contrib import admin
from .models import Users, Restaurant

# Register your models here.
# Models will appear in Django admin site
admin.site.register(Users)
admin.site.register(Restaurant)
