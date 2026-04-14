from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import AuthUserSerializer

class AuthUserList(generics.ListAPIView):
    """
    GET /api/auth-users/
    Returns [{"username":"alice"},…]
    Requires authentication.
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(is_active=True)
    serializer_class = AuthUserSerializer