from django.contrib import admin
from .import models

# Register your models here.
class HotelCategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',),}

class HotelCityAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',),}

admin.site.register(models.HotelCategories,HotelCategoriesAdmin)
admin.site.register(models.HotelCity,HotelCityAdmin)
admin.site.register(models.Hotel)
admin.site.register(models.Review)