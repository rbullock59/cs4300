from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import permissions, viewsets

from .models import Booking, Movie, Seat
from .serializers import BookingSerializer, MovieSerializer, SeatSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- Template (MVT) views ---

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account is ready.")
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})


@login_required
def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        seat = get_object_or_404(Seat, pk=seat_id, is_booked=False)
        Booking.objects.create(movie=movie, seat=seat, user=request.user)
        seat.is_booked = True
        seat.save(update_fields=['is_booked'])
        messages.success(request, f"Seat {seat.seat_number} booked for {movie.title}.")
        return redirect('booking_history')
    seats = Seat.objects.all()
    seats_available = seats.filter(is_booked=False).count()
    return render(request, 'bookings/seat_booking.html', {
        'movie': movie, 'seats': seats, 'seats_available': seats_available,
    })


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).select_related('movie', 'seat')
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if request.method == 'POST':
        movie_title, seat_number = booking.movie.title, booking.seat.seat_number
        booking.delete()
        messages.success(request, f"Cancelled seat {seat_number} for {movie_title}.")
    return redirect('booking_history')
