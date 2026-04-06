from django.contrib.auth.models import User
from rest_framework import serializers

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # expose only username
        fields = ('username')
