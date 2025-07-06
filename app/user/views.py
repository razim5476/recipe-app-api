"""
Views for the user API.
"""
from rest_framework import generics, permissions, authentication
from user.serializers import UserSerializer, AuthenticationToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user."""
    serializer_class = AuthenticationToken
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage authicated user."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self):
        """retreive and retur the authticated user."""
        return self.request.user
