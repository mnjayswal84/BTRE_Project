from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='listings'), #views.index is method name
    path('<int:listing_id>', views.listing, name='listing'), 
    path('search', views.search, name='search'),
    path('add_listing', views.add_listing, name='add_listing'),
]