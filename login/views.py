from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .models import User
from django.contrib.auth import authenticate, login, logout
from .permissions import IsAdminUser
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

import sys
# Create your views here.

class RegisterView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            print(created, file=sys.stderr)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Log the user in (Django session)
            login(request, user)
            
            # Generate or get token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # For session-based authentication
        logout(request)
        # For token-based authentication
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()

        return Response({"message": "Successfully logged out"}, status=status.HTTP_204_NO_CONTENT)


class PasswordResetVIEW(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('oldPassword')
        new_password = request.data.get('newPassword')

        # Check if old password is correct
        if not old_password or not new_password:
            return Response(
                {"error": "Both oldPassword and newPassword are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(old_password, user.password):
            return Response(
                {"error": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if check_password(new_password, new_password):
            return Response(
                {"error": "Old password and new are matched"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate the new password (you can add custom validation here)
        if len(new_password) < 5:  # Example: Check password length
            return Response(
                {"error": "New password must be at least 5 characters long."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update the user's password
        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password has been successfully updated."},
            status=status.HTTP_200_OK
        )

class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, many =True, format = None):
        print(f"auth : {request.auth}")
        users = User.objects.all()
        userSerializer = UserSerializer(users, many=True, context={"request" : request})
        return Response(userSerializer.data, status=status.HTTP_200_OK)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(request.user.password)
        return Response({
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })
    

@api_view(['GET'])
def api_root(request, format=None):
    print(f"request = : {request}")
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'profile': reverse('profile', request=request, format=format),
        'password-reset': reverse('password-reset', request=request, format=format),
        'login': reverse('login', request=request, format=format),
        'logout': reverse('logout', request=request, format=format),
        'register': reverse('register', request=request, format=format)
    })
