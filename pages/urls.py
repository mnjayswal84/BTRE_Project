from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), #views.index is method name
    path('about', views.about, name='about')
]