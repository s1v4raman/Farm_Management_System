import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FarmManagementSystem.settings')
django.setup()

from homepage.models import FarmExpense
from django.contrib.auth.models import User

def generate_dashboard_data():
    try:
        users = User.objects.all()
        if not users.exists():
            print("No users found in the database. Please create a superuser first.")
            return
    except Exception:
        print("Error fetching users.")
        return

    print("Clearing old farm expense data...")
    FarmExpense.objects.all().delete()
    
    print("Generating 6 months of daily dashboard data...")
    
    today = datetime.now().date()
    start_date = today - timedelta(days=180)
    seasons = ["Wheat Season", "Corn Winter", "Rice Monsoon", "Soybean Spring", "Tomato Summer"]
    
    records_created = 0
    for user in users:
        current_date = start_date
        while current_date <= today:
            seed_cost = Decimal(random.uniform(500.0, 2000.0)).quantize(Decimal('0.00'))
            fert_cost = Decimal(random.uniform(800.0, 3000.0)).quantize(Decimal('0.00'))
            labor_cost = Decimal(random.uniform(1000.0, 4000.0)).quantize(Decimal('0.00'))
            other_costs = Decimal(random.uniform(200.0, 1000.0)).quantize(Decimal('0.00'))
            
            total_investment = seed_cost + fert_cost + labor_cost + other_costs
            
            if random.random() < 0.15:
                crop_sale = (total_investment * Decimal(random.uniform(0.5, 0.9))).quantize(Decimal('0.00'))
            else:
                crop_sale = (total_investment * Decimal(random.uniform(1.2, 2.5))).quantize(Decimal('0.00'))
                
            season = random.choice(seasons)
            
            FarmExpense.objects.create(
                user=user,
                Expense_date=current_date,
                Season_or_crop=season,
                Seed_cost=seed_cost,
                Fertilizer_cost=fert_cost,
                Labor_cost=labor_cost,
                Other_costs=other_costs,
                Crop_sale=crop_sale
            )
            current_date += timedelta(days=1)
            records_created += 1
        
    print(f"Successfully generated {records_created} daily dashboard records from {start_date} to {today}!")

if __name__ == '__main__':
    generate_dashboard_data()
