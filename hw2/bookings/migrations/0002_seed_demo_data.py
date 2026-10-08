from datetime import date

from django.db import migrations

MOVIES = [
    ("Dune: Part Two", "Paul Atreides unites with the Fremen.", date(2024, 3, 1), 166),
    ("Oppenheimer", "The story of J. Robert Oppenheimer.", date(2023, 7, 21), 180),
    ("Spider-Man: Across the Spider-Verse", "Miles Morales returns.", date(2023, 6, 2), 140),
]

SEAT_NUMBERS = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]


def seed_demo_data(apps, schema_editor):
    Movie = apps.get_model('bookings', 'Movie')
    Seat = apps.get_model('bookings', 'Seat')
    for title, description, release_date, duration in MOVIES:
        Movie.objects.get_or_create(
            title=title,
            defaults={"description": description, "release_date": release_date, "duration": duration},
        )
    for seat_number in SEAT_NUMBERS:
        Seat.objects.get_or_create(seat_number=seat_number)


def remove_demo_data(apps, schema_editor):
    Movie = apps.get_model('bookings', 'Movie')
    Seat = apps.get_model('bookings', 'Seat')
    Movie.objects.filter(title__in=[m[0] for m in MOVIES]).delete()
    Seat.objects.filter(seat_number__in=SEAT_NUMBERS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_demo_data, remove_demo_data),
    ]
