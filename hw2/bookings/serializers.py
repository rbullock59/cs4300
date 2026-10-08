from rest_framework import serializers

from .models import Booking, Movie, Seat


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'duration']


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'is_booked']
        read_only_fields = ['is_booked']


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    seat_number = serializers.CharField(source='seat.seat_number', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'movie', 'movie_title', 'seat', 'seat_number', 'user', 'booking_date']
        read_only_fields = ['booking_date']

    def validate_seat(self, seat):
        if seat.is_booked:
            raise serializers.ValidationError("This seat is already booked.")
        return seat

    def create(self, validated_data):
        booking = super().create(validated_data)
        seat = booking.seat
        seat.is_booked = True
        seat.save(update_fields=['is_booked'])
        return booking
