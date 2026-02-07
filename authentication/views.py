from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from.serializers import LoginSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer, UserSerializer
from django.contrib.auth import authenticate
from django.conf import settings
import jwt
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from django.shortcuts import render
# Create your views here.



# Register API
class RegisterView(GenericAPIView):
    """Register a new user"""
    
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
             
            user = serializer.save()
            return Response({'user': UserSerializer(user).data}, status=201)
        return Response(serializer.errors, status=400)
    

# Login view
class LoginView(GenericAPIView):
    """Login a user  
    can use APIVIEW instead of GenericAPIVIEW TO Avoid creating another serializer for login 
    """

    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(email=email, username=username, password=password)
        if user:
            auth_token = jwt.encode({'username': user.username}, settings.JWT_SECRET_KEY)
            serializer = UserSerializer(user)
            data = {
                'user': serializer.data,
                'token': auth_token

            }
            return Response(data, status=status.HTTP_200_OK)
            #Send response
        return Response({'detail':'Invalid credentials'},
                             status=status.HTTP_401_UNAUTHORIZED)



#Password resets
class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)

        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://127.0.0.1:8000/api/auth/password-reset/confirm/{uid}/{token}/"

            message = f"Hi {user.username},\nClick below to reset your password:\n{reset_link}"

            send_mail(
                subject="Password Reset Request",
                message=message,
                from_email="noreply@example.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

        return Response({"message": "Reset link sent!"}, status=status.HTTP_200_OK)
#Password reset confirm 
class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password reset successful!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)