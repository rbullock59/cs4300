from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Booking, Movie, Seat


class MovieModelTests(APITestCase):
    def test_str_returns_title(self):
        movie = Movie.objects.create(
            title="Dune", description="Desert epic", release_date=date(2024, 1, 1), duration=155
        )
        self.assertEqual(str(movie), "Dune")


class SeatModelTests(APITestCase):
    def test_default_not_booked(self):
        seat = Seat.objects.create(seat_number="A1")
        self.assertFalse(seat.is_booked)


class BookingModelTests(APITestCase):
    def test_unique_seat_per_movie(self):
        user = User.objects.create_user(username="alice", password="pw12345")
        movie = Movie.objects.create(
            title="Dune", description="", release_date=date(2024, 1, 1), duration=155
        )
        seat = Seat.objects.create(seat_number="A1")
        Booking.objects.create(movie=movie, seat=seat, user=user)
        with self.assertRaises(Exception):
            Booking.objects.create(movie=movie, seat=seat, user=user)


class MovieApiTests(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Dune", description="Desert epic", release_date=date(2024, 1, 1), duration=155
        )

    def test_list_movies_is_public(self):
        url = '/api/movies/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], "Dune")

    def test_create_movie_requires_auth(self):
        url = '/api/movies/'
        response = self.client.post(url, {
            "title": "New Movie", "description": "", "release_date": "2024-02-02", "duration": 100,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_movie_authenticated(self):
        User.objects.create_user(username="bob", password="pw12345")
        self.client.login(username="bob", password="pw12345")
        url = '/api/movies/'
        response = self.client.post(url, {
            "title": "New Movie", "description": "", "release_date": "2024-02-02", "duration": 100,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BookingApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pw12345")
        self.movie = Movie.objects.create(
            title="Dune", description="", release_date=date(2024, 1, 1), duration=155
        )
        self.seat = Seat.objects.create(seat_number="A1")

    def test_booking_requires_auth(self):
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_booking_marks_seat_booked(self):
        self.client.login(username="alice", password="pw12345")
        url = reverse('booking-list')
        response = self.client.post(url, {"movie": self.movie.id, "seat": self.seat.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)

    def test_cannot_double_book_seat(self):
        self.client.login(username="alice", password="pw12345")
        url = reverse('booking-list')
        self.client.post(url, {"movie": self.movie.id, "seat": self.seat.id})
        response = self.client.post(url, {"movie": self.movie.id, "seat": self.seat.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_booking_history_only_shows_own_bookings(self):
        other = User.objects.create_user(username="carl", password="pw12345")
        Booking.objects.create(movie=self.movie, seat=self.seat, user=other)
        self.client.login(username="alice", password="pw12345")
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 0)


class TemplateViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pw12345")
        self.movie = Movie.objects.create(
            title="Dune", description="", release_date=date(2024, 1, 1), duration=155
        )
        self.seat = Seat.objects.create(seat_number="A1")

    def test_movie_list_page_loads(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dune")

    def test_seat_booking_requires_login(self):
        url = reverse('book_seat', args=[self.movie.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_seat_booking_flow(self):
        self.client.login(username="alice", password="pw12345")
        url = reverse('book_seat', args=[self.movie.id])
        response = self.client.post(url, {"seat_id": self.seat.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Booking.objects.filter(user=self.user, seat=self.seat).exists())

    def test_booking_history_page(self):
        self.client.login(username="alice", password="pw12345")
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        response = self.client.get(reverse('booking-history'))
        self.assertContains(response, "Dune")
