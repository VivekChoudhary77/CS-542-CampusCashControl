from rest_framework.views    import APIView
from rest_framework.response import Response
from django.db               import connection

class ReportDataView(APIView):
    def get(self, request):
        dept  = request.query_params.get('department','all_departments')
        month = request.query_params.get('month',     'all_months')
        year  = request.query_params.get('year',      'all_years')
        year_param = -1 if year=='all_years' else int(year)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM fetch_uploaded_data(%s,%s,%s)",
                [dept, month, year_param]
            )
            cols = [c[0] for c in cursor.description]
            data = [dict(zip(cols,row)) for row in cursor.fetchall()]

        return Response(data)