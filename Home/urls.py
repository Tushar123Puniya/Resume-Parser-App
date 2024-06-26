from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home_page, name='Home_page'),
    path('login', views.Login_page, name='Login_page'),
    path('signup', views.Signup_page, name='Signup_page'),
    path('password_reset', views.Passwordreset_page, name='Passwordreset_page'),
    path('option', views.Option_page, name='Option_page'),
    path('parsing', views.Parsing_page, name='Parsing_page'),
    path('scoring', views.Scoring_page, name='Scoring_page'),
]
