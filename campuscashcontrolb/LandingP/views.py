from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class DashboardData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return dummy data for the dashboard
        return Response({"message": "Dashboard data placeholder"})