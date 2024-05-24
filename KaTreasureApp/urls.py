from django.urls import path, include
from KaTreasureApp.backend import views, auth

app_name = 'KaTreasureApp'

urlpatterns = [
    path('base', views.base, name='base'),
    path('', views.home, name='home'),
    path('signin', auth.login, name='login'),
    path('signup', auth.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('contactus', views.contactus, name='contactus'),
]
