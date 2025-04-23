from django.urls import path
from .views import ReportDataView

urlpatterns = [
  path('', ReportDataView.as_view(), name='report-data'),
]