from django.db import models
from user.models import user  # Custom user model
from hotel.models import Hotel
from django.core.exceptions import ValidationError


BOOKING_STATUS = [
    ('Completed', 'Completed'),
    ('Pending', 'Pending')
]

class Booking(models.Model):
    users = models.ForeignKey(user, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    status = models.CharField(choices=BOOKING_STATUS, max_length=10, default="Pending")
    cancel = models.BooleanField(default=False)

    