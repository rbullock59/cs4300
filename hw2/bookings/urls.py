from django.urls import path

from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/book/', views.seat_booking, name='book_seat'),
    path('bookings/history/', views.booking_history, name='booking-history'),
]
