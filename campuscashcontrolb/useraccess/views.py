from django.contrib.auth.models import User
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class AuthUserList(generics.ListAPIView):
    """
    GET /api/auth-users/
    Returns [{"username":"alice"},…]
    Requires authentication.
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(is_active=True)
    serializer_class = AuthUserSerializer