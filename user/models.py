from django.db import models
from django.contrib.auth.models import User

class user(models.Model):
    users=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='user/images/')
    mobile_no=models.CharField(max_length=12)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.users.first_name}{self.users.last_name}"
   
