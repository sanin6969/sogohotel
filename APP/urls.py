from django.urls import path,include
from .views import *

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('rooms',rooms,name='rooms'),
    path('about',about,name='about'),
    path('single_room',single_room,name='single_room'),
    path('payment',payment,name='payment'),
    path('book/<int:room_id>/', book_room, name='book_room'),
    path('payment/', payment_page, name='payment_page'),
    path('process_payment/', process_payment, name='process_payment'),
    path('booking_complete/', booking_complete, name='booking_complete'),
    path('payment_failed/', payment_failed, name='payment_failed'),
    path('dummy_payment_gateway/', dummy_payment_gateway, name='dummy_payment_gateway'),
    path('payment_success/', payment_success, name='payment_success'),
    path('tickets/', tickets, name='tickets'),
]