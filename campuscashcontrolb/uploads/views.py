import os
import pandas as pd
import tempfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

@csrf_exempt  # In production, secure this endpoint properly.
def upload_financial_data(request):
    if request.method == 'POST':
        # Retrieve metadata from POST data
        department = request.POST.get('department')
        month = request.POST.get('month')
        year = request.POST.get('year')
        uploaded_file = request.FILES.get('file')

        if not all([department, month, year, uploaded_file]):
            return JsonResponse({'error': 'Missing required fields.'}, status=400)

        try:
            # Save file to a temporary file path.
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            # Determine the file extension (lowercase)
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()

            # Read data into a DataFrame using Pandas.
            if file_ext == '.csv':
                df = pd.read_csv(tmp_path)
            elif file_ext in ['.xlsx', '.xlsm']:
                df = pd.read_excel(tmp_path, engine='openpyxl')
            elif file_ext == '.xls':
                # For .xls files, use xlrd engine
                df = pd.read_excel(tmp_path, engine='xlrd')
            else:
                os.remove(tmp_path)
                return JsonResponse({'error': 'Unsupported file format.'}, status=400)

            # Check if the required columns are present.
            if 'Items' not in df.columns or 'Revenue' not in df.columns:
                os.remove(tmp_path)
                return JsonResponse({'error': 'Invalid template format. Expected columns "Items" and "Revenue".'}, status=400)

            # Check if the DataFrame is empty or if any row in Items or Revenue is missing.
            if df.empty:
                os.remove(tmp_path)
                return JsonResponse({'error': 'Uploaded file is empty.'}, status=400)

            # Validate every row: if any row has missing Items or Revenue, reject the upload.
            for index, row in df.iterrows():
                if pd.isna(row['Items']) or pd.isna(row['Revenue']) or str(row['Items']).strip() == '' or str(row['Revenue']).strip() == '':
                    os.remove(tmp_path)
                    return JsonResponse({'error': 'There are some empty values or missing data in Items/Revenue.'}, status=400)

            # All validations passed: iterate over rows and insert into database using the stored procedure.
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    item = row['Items']
                    revenue = row['Revenue']
                    cursor.execute("""
                        CALL insert_uploaded_data(%s::VARCHAR, %s::VARCHAR, %s::INTEGER, %s::VARCHAR, %s::NUMERIC);
                    """, [department, month, int(year), str(item), revenue])

            # Remove the temporary file
            os.remove(tmp_path)
            return JsonResponse({'message': 'Data uploaded successfully.'})
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)