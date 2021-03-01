from .views import VerificationView #, LoginView     #, Username
from .views import register
from django.urls import path

from . import views

urlpatterns = [
    #path('register', LoginView.as_view(), name='register'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'), 
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),    
    path('activate/<uidb64>/<token>', VerificationView.as_view(),name='activate'),
]