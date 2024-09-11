from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def custom_api_root(request, format=None):
    return Response({
        'service': reverse('service-list', request=request, format=format),
        'contact_us': reverse('contactus-list', request=request, format=format),
        'user': reverse('user-list', request=request, format=format),
        'hotel': reverse('hotel-list', request=request, format=format),
    }, status=status.HTTP_200_OK)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', custom_api_root, name='api-root'),  # Custom API root
    path('', include('contact_us.urls')),  # Include contact_us routes
    path('', include('service.urls')),  # Include service routes
    path('', include('user.urls')),  # Include service routes
    path('', include('hotel.urls')),  # Include service routes
    path('', include('bookings.urls')),  # Include service routes
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
