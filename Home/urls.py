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
    path('otp_verification', views.verify_otp, name='verify_otp'),
    path('user_details', views.user_detail, name='user_detail'),
    path('change_password', views.change_password, name='change_password'),
    path('account', views.Account_page, name='Account_page'),
    path('verify_otp', views.verify_otp1, name='verify_otp1'),
]
