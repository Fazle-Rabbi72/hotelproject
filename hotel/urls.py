from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'hotels', views.HotelViewset)
router.register(r'hotel-categories', views.HotelCategoriesViewset)
router.register(r'hotel-city', views.HotelCityViewset)
router.register(r'hotel/reviews', views.ReviewViewset)

urlpatterns = [
    path('', include(router.urls)),
]


