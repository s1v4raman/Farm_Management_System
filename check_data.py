import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FarmManagementSystem.settings')
django.setup()

from homepage.models import Milk_production, Eggs_production

print(f"Total Milk_production records: {Milk_production.objects.count()}")
print(f"Total Eggs_production records: {Eggs_production.objects.count()}")

if Milk_production.objects.exists():
    print("\nSome Milk_production records:")
    for r in Milk_production.objects.all()[:5]:
        print(f"Year: {r.Year}, Month: {r.Month}, Day: {r.Day}, Total Prod: {r.Total_production}")

if Eggs_production.objects.exists():
    print("\nSome Eggs_production records:")
    for r in Eggs_production.objects.all()[:5]:
        print(f"Year: {r.Year}, Month: {r.Month}, Day: {r.Day}, Total Eggs: {r.Total_egg_collection}")
