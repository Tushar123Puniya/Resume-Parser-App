from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home_page, name='Home_page'),
    path('login', views.Login_page, name='Login_page'),
    path('signup', views.Signup_page, name='Signup_page'),
    path('aboutus', views.AboutUs_page, name='AboutUs_page'),
    path('contactus', views.ContactUs_page, name='ContactUs_page'),
    path('parsing', views.Parsing_page, name='Parsing_page'),
]
