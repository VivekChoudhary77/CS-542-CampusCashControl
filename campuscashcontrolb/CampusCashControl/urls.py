"""
URL configuration for CampusCashControl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
# from django.urls import path, include
# from django.http import HttpResponseRedirect
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('api.urls')),  # Your API endpoints
#     path('', lambda request: HttpResponseRedirect('/api/')),  # Redirect / to /api/
# ]

from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("accounts.urls")),  # Django API
    path('api/', include('uploads.urls')),
    path("", RedirectView.as_view(url="http://localhost:8080/", permanent=False)),  # Redirect to Vue
    path('api/', include('departments.urls')),
    path('api/reports/', include('reports.urls')),
]

