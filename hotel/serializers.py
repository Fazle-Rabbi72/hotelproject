from rest_framework import serializers
from . import models

class HotelSerializers(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    category_name = serializers.CharField(source='categories.name', read_only=True)
    class Meta:
        model = models.Hotel
        fields = '__all__'

class HotelCategoriesSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = models.HotelCategories
        fields = '__all__'  
        
        
class HotelCitySerializers(serializers.ModelSerializer):
    
    class Meta:
        model = models.HotelCity
        fields = '__all__'
 
class ReviewSerializers(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()  # Use SerializerMethodField for custom field
    reviewer_image = serializers.ImageField(source='reviewer.image', read_only=True)
    hotel_name = serializers.CharField(source='hotel.title', read_only=True)

    class Meta:
        model = models.Review
        fields = '__all__'

    def get_reviewer_name(self, obj):
        return obj.reviewer.users.username  # Assuming 'reviewer' is related to the 'User' model