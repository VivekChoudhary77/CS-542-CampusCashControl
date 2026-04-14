from django.urls import path
from .views import AuthUserList

urlpatterns = [
    path('auth-users/', AuthUserList.as_view(), name='auth-users'),
]
