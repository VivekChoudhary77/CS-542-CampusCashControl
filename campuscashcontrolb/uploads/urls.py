from django.urls import path
from .views import upload_financial_data

urlpatterns = [
    path('upload/', upload_financial_data, name='upload_financial_data'),
]