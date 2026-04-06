import pandas as pd
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Export the uploaded_data view to CSV for Tableau"

    def handle(self, *args, **options):
        # Your exact SQL query:
        query = "SELECT * FROM uploaded_data;"

        # Use Django's DB connection under the hood
        df = pd.read_sql_query(query, connection)

        # Where to save the file
        export_dir = Path(settings.BASE_DIR) / "public_exports"
        export_dir.mkdir(exist_ok=True)

        csv_path = export_dir / "exported_data.csv"
        df.to_csv(csv_path, index=False)

        self.stdout.write(self.style.SUCCESS(
            f"Exported {len(df)} rows to {csv_path}"
        ))
