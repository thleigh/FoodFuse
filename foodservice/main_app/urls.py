from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('user/<username>/', views.profile, name='profile'),
    path('favorites/', views.favorites_index, name='favorites'),
    path('favorites/<int:restaurant_id>', views.favorites_show, name='favorites_show'),
    path('data/', views.data, name='data'),
    # path('scraper/', views.scraper_function, name='scraper'),
    # path('restaurants/create/', views.RestaurantCreate.as_view(), name='restaurant_create'),
    # path('restaurants/<int:pk>/update/', views.RestaurantUpdate.as_view(), name='restaurant_update'),
    # path('restaurants/<int:pk>/delete/', views.RestaurantDelete.as_view(), name='restaurant_delete'),
    # path('data/', views.datapage, name='data'),
    # path('favorites/create/', views.RestaurantCreate.as_view(), name='restaurant_create'),
    # path('favorites/<int:pk>/update/', views.RestaurantUpdate.as_view(), name='restaurant_update'),
    # path('favorites/<int:pk>/delete/', views.RestaurantDelete.as_view(), name='restaurant_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

