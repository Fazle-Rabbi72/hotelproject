from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class userSerializer(serializers.ModelSerializer):
    
    user_name = serializers.SerializerMethodField()  # to show user name 
    
    class Meta:
        model = models.user
        fields = '__all__'

    def get_user_name(self, obj):
        return obj.users.username  
class ResistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(required=True)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password','confirm_password']
    
    def save(self):
        username=self.validated_data['username']
        email=self.validated_data['email']
        first_name=self.validated_data['first_name']
        last_name=self.validated_data['last_name']
        password1=self.validated_data['password']
        password2=self.validated_data['confirm_password']

        if password1!=password2:
            raise serializers.ValidationError({'error':"password Dosen't matched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email Already Exsits"})
        account=User(username=username,first_name=first_name,last_name=last_name,email=email)
        account.set_password(password1)
        account.is_active=False
        account.save()
        return account
    
class UserLoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)