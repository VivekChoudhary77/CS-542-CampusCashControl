from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import AuthUserSerializer

class AuthUserList(generics.ListAPIView):
    """
    GET /api/auth-users/
    Returns [{"id":1,"username":"alice"},…]
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = AuthUserSerializer