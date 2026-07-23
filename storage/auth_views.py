import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import request, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .auth_serializers import UserSerializer
from django.contrib.auth.models import User 


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to include user info in token response."""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add user info to response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login endpoint that returns JWT tokens and user info."""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username') or request.data.get('username')
        password = request.query_params.get('password') or request.data.get('password')
        if not username or not password:
            return Response(
                {
                    'error': 'GET requires username and password either as query parameters or in the request body',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data={
            'username': username,
            'password': password,
        })
        serializer.is_valid(raise_exception=True)
        response_data = serializer.validated_data
        response_data['message'] = 'Login successful'
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data['message'] = 'Login successful'
        return response
    



class RegisterView(APIView):
    """Registration endpoint that returns JWT tokens."""
    permission_classes = [AllowAny]

    # def get (self, request):
    #     """Get all users (for testing purposes)."""
    #     users = User.objects.all()
    #     serializer = UserSerializer(users, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create new user and return JWT tokens."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate JWT tokens for the new user
            token_serializer = CustomTokenObtainPairSerializer(data={
                'username': request.data.get('username'),
                'password': request.data.get('password'),
            })
            if token_serializer.is_valid():
                return Response({
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data,
                    'access': token_serializer.validated_data['access'],
                    'refresh': token_serializer.validated_data['refresh'],
                }, status=status.HTTP_201_CREATED)
            return Response({'error': 'Failed to generate tokens'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    class ProfileView(APIView):
     
#      """Get current user profile."""
#      permission_classes = [IsAuthenticated]

#      def get(self, request):        
#          serializer = UserSerializer(request.user)
#          return Response(serializer.data, status=status.HTTP_200_OK)
 
class TokenRefreshView(TokenRefreshView):
    """Endpoint to refresh JWT access token using refresh token."""
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        refresh = request.query_params.get('refresh')
        if not refresh:
            return Response(
                {'error': 'GET requires a refresh token query parameter: refresh'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data={'refresh': refresh})
        serializer.is_valid(raise_exception=True)
        response_data = {
            'message': 'Token refreshed successfully',
            **serializer.validated_data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data['message'] = 'Token refreshed successfully'
        return response
    
   