from django.contrib import admin
from . import models

class userAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'mobile_no', 'image']

    def first_name(self, obj):
        return obj.users.first_name
   
    def last_name(self, obj):
        return obj.users.last_name
   

admin.site.register(models.user, userAdmin)