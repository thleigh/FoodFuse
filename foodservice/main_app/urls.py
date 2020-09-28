from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('test/', views.testfrontpage, name='testfrontpage'),
    path('signup/', views.signup_view, name='signup'),
    path('user/<username>/', views.profile, name='profile'),
<<<<<<< HEAD
=======
    # path('data/', views.datapage, name='data'),
>>>>>>> 8272c206d393fc4f9e0d5d1f5054ba4500dee77e
]