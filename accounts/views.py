from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import RegisterSerializer, UserProfileSerializer, UserSerializer
from .models import UserProfile
from django.db.models import Q

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'message': 'Registration successful!',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)

        # 🔍 Log errors to console
        print("Registration Error:", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        login_identifier = request.data.get('username')  # This could be email or username
        password = request.data.get('password')
        
        # First try to see if the login identifier is an email
        try:
            # Check if user exists with this email
            user = User.objects.get(email=login_identifier)
            # If found, authenticate with username and password
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                token, _ = Token.objects.get_or_create(user=auth_user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # If no user found with that email, try username authentication
            auth_user = authenticate(username=login_identifier, password=password)
            if auth_user:
                token, _ = Token.objects.get_or_create(user=auth_user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get the authenticated user's information"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_or_create_profile(self, user):
        """Get or create user profile"""
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            # Create a new profile if it doesn't exist
            return UserProfile.objects.create(user=user)
    
    def get(self, request):
        """Get the user's profile"""
        profile = self.get_or_create_profile(request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request):
        """Update the user's profile"""
        profile = self.get_or_create_profile(request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
