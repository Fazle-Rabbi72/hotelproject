from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='users.users.username', read_only=True)
    hotel_name = serializers.CharField(source='hotel.title', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        # Check if the hotel is already booked
        if Booking.objects.filter(hotel=data['hotel']).exists():
            raise serializers.ValidationError("This hotel has already been booked by another user.")
        
        # Check if the user has enough balance
        if data['users'].balance < data['hotel'].price:
            raise serializers.ValidationError("Insufficient balance to complete booking.")
        
        return data