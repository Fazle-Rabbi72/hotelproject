from django.shortcuts import render
from rest_framework import viewsets,pagination,filters
from .import models
from .import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class HotelPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100
class HotelViewset(viewsets.ModelViewSet):
    queryset = models.Hotel.objects.all()
    serializer_class = serializers.HotelSerializers
    pagination_class = HotelPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['city__name', 'categories__name', 'title'] 
    

class HotelCategoriesViewset(viewsets.ModelViewSet):
    queryset = models.HotelCategories.objects.all()
    serializer_class = serializers.HotelCategoriesSerializers

class HotelCityViewset(viewsets.ModelViewSet):
    queryset = models.HotelCity.objects.all()
    serializer_class = serializers.HotelCitySerializers

class ReviewViewset(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializers 

    def get_queryset(self):
        queryset = super().get_queryset()
        hotel_id = self.request.query_params.get('hotel_id', None)
        if hotel_id is not None:
            queryset = queryset.filter(hotel_id=hotel_id)
        return queryset