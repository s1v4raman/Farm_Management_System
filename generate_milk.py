import os
import django
import random
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FarmManagementSystem.settings') # Replace if different
django.setup()

from homepage.models import Milk_production
from django.contrib.auth.models import User

def generate_data():
    # Ensure there's a user
    user = User.objects.first()
    if not user:
        user = User.objects.create_user(username='admin', password='password')

    years = [2024, 2025, 2026]
    
    # Delete existing to prevent duplication if script is run multiple times
    Milk_production.objects.all().delete()

    records_to_create = []

    for year in years:
        for month in range(1, 13):
            # Stop generating future data in 2026 if desired, but let's just do up to March
            if year == 2026 and month > 3:
                continue

            days_to_gen = list(range(1, 15))  # Minimum 10 data, let's do 14 days per month
            
            # Make sure we hit the present day (2026-03-23)
            if year == 2026 and month == 3:
                days_to_gen.append(23)
                
            for day in set(days_to_gen):
                record = Milk_production(
                    user=user,
                    Year=year,
                    Month=month,
                    Day=day,
                    Livestock_number=random.randint(10, 50),
                    Morning_production=Decimal(round(random.uniform(50.0, 100.0), 2)),
                    Midday_production=Decimal(round(random.uniform(30.0, 70.0), 2)),
                    Evening_production=Decimal(round(random.uniform(40.0, 80.0), 2)),
                    Morning_consumption=Decimal(round(random.uniform(20.0, 40.0), 2)),
                    Evening_consumption=Decimal(round(random.uniform(25.0, 45.0), 2)),
                )
                
                # Calling save() is required to trigger total calculation overriding in model
                record.save()
                
    print(f"Successfully generated {Milk_production.objects.count()} records!")

if __name__ == "__main__":
    generate_data()
