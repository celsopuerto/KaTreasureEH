from django.urls import path, include
from KaTreasureApp.backend import views
from KaTreasureApp.backend import auth

app_name = 'KaTreasureApp'

urlpatterns = [
    path('base', views.base, name='base'),
    path('', views.home, name='home'),
    path('signup', auth.signup, name='signup'),
    path('login', auth.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('contactus', views.contactus, name='contactus'),
]
