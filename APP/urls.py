from django.urls import path,include
from .views import *

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('rooms',rooms,name='rooms'),
    path('about',about,name='about'),
    path('single_room',single_room,name='single_room'),
    path('payment',payment,name='payment'),
]