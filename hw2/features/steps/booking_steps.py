from datetime import date

from behave import given, then, when
from django.contrib.auth.models import User
from django.urls import reverse

from bookings.models import Booking, Movie, Seat


@given('a movie "{title}" with 1 available seat "{seat_number}"')
def step_create_movie_and_seat(context, title, seat_number):
    context.movie = Movie.objects.create(
        title=title, description="", release_date=date(2024, 1, 1), duration=120
    )
    context.seat = Seat.objects.create(seat_number=seat_number)


@given('I am logged in as "{username}"')
def step_login(context, username):
    context.user = User.objects.create_user(username=username, password="pw12345")
    context.test.client.login(username=username, password="pw12345")


@given('seat "{seat_number}" for "{title}" is already booked')
def step_seat_already_booked(context, seat_number, title):
    seat = Seat.objects.get(seat_number=seat_number)
    movie = Movie.objects.get(title=title)
    other = User.objects.create_user(username="bob_other", password="pw12345")
    Booking.objects.create(movie=movie, seat=seat, user=other)
    seat.is_booked = True
    seat.save(update_fields=['is_booked'])


@when('I visit the movie list page')
def step_visit_movie_list(context):
    context.response = context.test.client.get(reverse('movie_list'))


@when('I visit the seat booking page for "{title}"')
def step_visit_seat_booking(context, title):
    movie = Movie.objects.get(title=title)
    context.response = context.test.client.get(reverse('book_seat', args=[movie.id]))


@when('I book seat "{seat_number}" for "{title}"')
def step_book_seat(context, seat_number, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(seat_number=seat_number)
    context.response = context.test.client.post(
        reverse('book_seat', args=[movie.id]), {"seat_id": seat.id}
    )


@then('I should see "{text}" on the page')
def step_should_see(context, text):
    assert text.encode() in context.response.content, f"{text!r} not found in response"


@then('the seat "{seat_number}" should be marked as booked')
def step_seat_booked(context, seat_number):
    seat = Seat.objects.get(seat_number=seat_number)
    assert seat.is_booked is True


@then('my booking history should contain "{title}"')
def step_booking_history(context, title):
    response = context.test.client.get(reverse('booking_history'))
    assert title.encode() in response.content


@then('I should not be able to select seat "{seat_number}"')
def step_cannot_select_seat(context, seat_number):
    seat = Seat.objects.get(seat_number=seat_number)
    assert seat.is_booked is True
    assert b'disabled' in context.response.content
