from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('check/otp', views.Check_otpView.as_view(), name='check_otp'),
    path('logout', views.logout, name='logout'),
    path('add_address', views.AddAddressView.as_view(), name='add_address')
]