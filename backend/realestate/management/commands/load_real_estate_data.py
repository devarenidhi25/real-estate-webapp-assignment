"""
Management command to load real estate data from Excel into the database.
Replaces startup-time Excel loading with a scheduled/on-demand load.

Usage:
    python manage.py load_real_estate_data
"""

import pandas as pd
import boto3
from io import BytesIO
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from realestate.models import RealEstateData


class Command(BaseCommand):
    help = 'Load real estate data from Excel file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading',
        )

    def handle(self, *args, **options):
        try:
            # Load Excel data from S3
            self.stdout.write(self.style.WARNING('Loading Excel file from S3...'))
            df = self._load_excel_from_s3()

            if df.empty:
                self.stdout.write(self.style.ERROR('Excel file is empty'))
                return

            # Clear existing data if requested
            if options['clear']:
                self.stdout.write(self.style.WARNING('Clearing existing data...'))
                RealEstateData.objects.all().delete()

            # Load data into database
            self.stdout.write(self.style.WARNING(f'Loading {len(df)} rows into database...'))
            self._load_data_to_db(df)

            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Successfully loaded {len(df)} records into database'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error loading data: {str(e)}')
            )
            raise

    def _load_excel_from_s3(self) -> pd.DataFrame:
        """Load Excel file from S3."""
        try:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
                region_name="eu-north-1"
            )

            response = s3.get_object(
                Bucket="real-estate-fa1-bucket",
                Key="Sample_data.xlsx"
            )

            df = pd.read_excel(BytesIO(response["Body"].read()))

            # Verify required columns exist
            required_columns = ["final location", "year"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                raise ValueError(
                    f"Missing required columns: {missing_columns}\n"
                    f"Available columns: {list(df.columns)}"
                )

            # Clean column names and data
            df.columns = df.columns.str.strip()

            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].str.strip()

            return df

        except Exception as e:
            raise Exception(f"Error loading Excel from S3: {str(e)}")

    def _load_data_to_db(self, df: pd.DataFrame):
        """Load data from DataFrame into database using bulk_create."""
        # Find price and demand columns
        price_col = self._get_price_column(df)
        demand_col = self._get_demand_column(df)

        if not price_col:
            raise ValueError("Could not find price column in Excel file")

        if not demand_col:
            raise ValueError("Could not find demand column in Excel file")

        # Prepare records for bulk insertion
        records = []

        for _, row in df.iterrows():
            try:
                area = str(row['final location']).strip()
                year = int(row['year'])
                price = float(row[price_col])
                demand = int(row[demand_col]) if pd.notna(row[demand_col]) else 0

                record = RealEstateData(
                    area=area,
                    year=year,
                    price=price,
                    demand=demand
                )
                records.append(record)

            except (ValueError, KeyError, TypeError) as e:
                self.stdout.write(
                    self.style.WARNING(f'Skipping row due to error: {str(e)}')
                )
                continue

        # Bulk insert all records
        if records:
            with transaction.atomic():
                RealEstateData.objects.bulk_create(records, batch_size=1000)

    def _get_price_column(self, df: pd.DataFrame) -> str:
        """Find the price column in the dataframe."""
        possible_names = [
            "flat - weighted average rate",
            "flat-weighted average rate",
            "weighted average rate",
            "price",
            "rate"
        ]

        for col in df.columns:
            if col.lower() in [name.lower() for name in possible_names]:
                return col

        # Return first column with 'rate' or 'price' in name
        for col in df.columns:
            if 'rate' in col.lower() or 'price' in col.lower():
                return col

        return None

    def _get_demand_column(self, df: pd.DataFrame) -> str:
        """Find the demand column in the dataframe."""
        possible_names = [
            "total units",
            "total_sales - igr",
            "total_sales-igr",
            "total sales",
            "units",
            "demand"
        ]

        for col in df.columns:
            if col.lower() in [name.lower() for name in possible_names]:
                return col

        # Return first column with 'unit' or 'sales' in name
        for col in df.columns:
            if 'unit' in col.lower() or 'sales' in col.lower():
                return col

        return None
