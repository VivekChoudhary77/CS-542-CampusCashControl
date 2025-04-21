from django.urls import path, include
from django.contrib import admin
from . import views  # Make sure to import views
#from  .views import UserListCreateView

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path('admin/', admin.site.urls),
    path('api/', include('departments.urls')),
    #path('api/users/', UserListCreateView.as_view(), name='user-create'),
    #path('departments/', views.department_list, name='department-list'),
]


