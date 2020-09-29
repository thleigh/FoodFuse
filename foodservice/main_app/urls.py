from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('test/', views.testfrontpage, name='testfrontpage'),
    path('signup/', views.signup_view, name='signup'),
    path('user/<username>/', views.profile, name='profile'),
    path('favorites/', views.favorites, name='favorites'),
    # path('data/', views.datapage, name='data'),
    # path('restaurants/create/', views.RestaurantCreate.as_view(), name='restaurant_create'),
    # path('restaurants/<int:pk>/update/', views.RestaurantUpdate.as_view(), name='restaurant_update'),
    # path('restaurants/<int:pk>/delete/', views.RestaurantDelete.as_view(), name='restaurant_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)