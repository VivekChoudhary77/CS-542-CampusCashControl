from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

from .models import Department
from .serializers import DepartmentSerializer

class DepartmentListView(APIView):
    def get(self, request):
        departments = Department.objects.all().order_by('id')
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

class DepartmentManageView(APIView):
    def post(self, request):
        data = request.data
        op_type = data.get('operation')
        dept_id = data.get('id') or None
        dept_name = data.get('name')

        with connection.cursor() as cursor:
            cursor.callproc('manage_department', [op_type, dept_id, dept_name, 1])  # user_id = 1 as example

        return Response({'message': f'{op_type} operation successful'}, status=status.HTTP_200_OK)

class ActiveDepartmentsView(APIView):
    def get(self, request):
        active_departments = Department.objects.filter(is_active=True).order_by('name')
        serializer = DepartmentSerializer(active_departments, many=True)
        return Response(serializer.data)
