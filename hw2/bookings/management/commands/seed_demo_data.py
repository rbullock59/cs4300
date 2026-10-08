from datetime import date

from django.core.management.base import BaseCommand

from bookings.models import Movie, Seat

MOVIES = [
    ("Dune: Part Two", "Paul Atreides unites with the Fremen.", date(2024, 3, 1), 166),
    ("Oppenheimer", "The story of J. Robert Oppenheimer.", date(2023, 7, 21), 180),
    ("Spider-Man: Across the Spider-Verse", "Miles Morales returns.", date(2023, 6, 2), 140),
]

SEAT_NUMBERS = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]


class Command(BaseCommand):
    help = "Seed the database with sample movies and seats for demo purposes."

    def handle(self, *args, **options):
        for title, description, release_date, duration in MOVIES:
            Movie.objects.get_or_create(
                title=title,
                defaults={"description": description, "release_date": release_date, "duration": duration},
            )
        for seat_number in SEAT_NUMBERS:
            Seat.objects.get_or_create(seat_number=seat_number)
        self.stdout.write(self.style.SUCCESS("Seeded demo movies and seats."))
