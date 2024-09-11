from django.shortcuts import render,redirect
from rest_framework import viewsets
from .import models
from .import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import user
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
# for email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class UserViewset(viewsets.ModelViewSet):
    queryset = models.user.objects.all()
    serializer_class = serializers.userSerializer



class DepositView(APIView):
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')  # Get user_id from request data
        deposit_amount = request.data.get('amount')

        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = get_object_or_404(user, id=user_id)


        try:
            # Convert deposit_amount to a Decimal and validate it
            deposit_amount = Decimal(deposit_amount)
            if deposit_amount <= 0:
                return Response({"error": "Deposit amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

            # Update user's balance
            user_profile.balance += deposit_amount
            user_profile.save()

            return Response({"message": "Amount deposited successfully!", "new_balance": user_profile.balance}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class UserRegistrationView(APIView):
    serializer_class=serializers.ResistrationSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid():
          user=serializer.save()
          token=default_token_generator.make_token(user)
          print("token",token)
          uid=urlsafe_base64_encode(force_bytes(user.pk))
          print("uid",uid)
          confirm_link=f"http://127.0.0.1:8000/register/active/{uid}/{token}/"
          email_subject="Confirm Your Email"
          email_body=render_to_string('confirm_email.html',{"confirm_link":confirm_link})
          email=EmailMultiAlternatives(email_subject,'',to=[user.email])
          email.attach_alternative(email_body,"text/html")
          email.send()
          return Response("Check your email") 
        return Response(serializer.errors) 
def active(self,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=User._default_manager.get(pk=uid)
    except(User.DoseNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

class UserLoginApiView(APIView):
    def post(self,request):
        serializer=serializers.UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')


            user= authenticate(username=username,password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request,user)
                custom_user = user.user 
                print("user",custom_user.id)
                return Response({'token':token.key,'user_id':custom_user.id})
            else:
                return Response({'error':"Invalid Credential"})
        return Response(serializer.errors)
    
class LogoutAPIview(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
