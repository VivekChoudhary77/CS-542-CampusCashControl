from django.urls import path
from .views import DepartmentListView, DepartmentManageView, ActiveDepartmentsView

urlpatterns = [
    path('departments/', DepartmentListView.as_view()),
    path('manage-department/', DepartmentManageView.as_view()),
    path('departments/active/', ActiveDepartmentsView.as_view()),
]
