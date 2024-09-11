from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.permissions import IsAuthenticated

class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        users_id = self.request.query_params.get('users_id', None)
        if users_id is not None:
            queryset = queryset.filter(users_id=users_id)
        return queryset
  
    def get_queryset(self):
        queryset = super().get_queryset()
        hotel_id = self.request.query_params.get('hotel_id', None)
        if hotel_id is not None:
            queryset = queryset.filter(hotel_id=hotel_id)
        return queryset
    
    def create(self, request, *args, **kwargs):
        try:
            return super(BookingViewSet, self).create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    