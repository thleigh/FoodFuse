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
    # path('data/', views.datapage, name='data'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)