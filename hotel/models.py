from django.db import models
from user.models import user
# Create your models here.
class HotelCategories(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True)
    def __str__(self) -> str:
        return self.name
    
class HotelCity(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True)
    def __str__(self) -> str:
        return self.name
    
class Hotel(models.Model):
    city = models.ForeignKey(HotelCity, on_delete=models.CASCADE, default=1,related_name='hotels')
    title=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    description=models.CharField(max_length=500)
    price=models.IntegerField()
    image=models.ImageField(upload_to='book/media/uploads/',blank=True,null=True)
    categories= models.ForeignKey(HotelCategories, on_delete=models.CASCADE, default=1,related_name='hotels')
    def __str__(self) -> str:
        return self.title

STER_CHOICE=[
    ('⭐','⭐'),
    ('⭐⭐','⭐⭐'),
    ('⭐⭐⭐','⭐⭐⭐'),
    ('⭐⭐⭐⭐','⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐','⭐⭐⭐⭐⭐'),
]
class Review(models.Model):
    reviewer=models.ForeignKey(user,on_delete=models.CASCADE)
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    body=models.TextField()
    created=models.TimeField(auto_now_add=True)
    rating=models.CharField(choices=STER_CHOICE,max_length=100)

    def __str__(self):
        return f"User:{self.reviewer.users.first_name}; Hotel:{self.hotel.title} "