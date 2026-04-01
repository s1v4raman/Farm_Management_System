import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FarmManagementSystem.settings')
django.setup()

from homepage.models import (
    Retail_Crop_Sales,
    Retail_Egg_Sales,
    Retail_Milk_Sales,
    Retail_Machinery_Renting,
    Retail_Livestock_Sales,
)
from django.contrib.auth.models import User

def generate_retail_data():
    try:
        users = User.objects.all()
        if not users.exists():
            print("No users found in the database. Please create a superuser first.")
            return
    except Exception:
        print("Error fetching users.")
        return

    start_date = datetime.now().date() - timedelta(days=60)
    customers = ["Rahul Singh", "Anita Patel", "Suresh Kumar", "Farm to Home", "AgriCorp", "Mandi Traders", "Local Grocery", "Green Leaf Co.", "Fresh Mart", "John Doe"]
    payments = ['Cash', 'Card', 'UPI']
    
    crop_names = ["Wheat", "Rice", "Sugarcane", "Cotton", "Maize", "Turmeric", "Onion"]
    milk_prices = [55.00, 60.00, 65.00, 70.00]
    machinery = ["Tractor", "Harvester", "Seeder", "Plough", "Sprayer"]
    services = ["Field Ploughing", "Harvesting", "Seeding", "Chemical Spraying", "Land Leveling"]
    livestock = [("Cow", "Holstein"), ("Cow", "Jersey"), ("Buffalo", "Murrah"), ("Goat", "Boer"), ("Sheep", "Merino")]

    records_count = 0

    print("Generating Mock Retail Data for all users...")

    for user in users:
        for i in range(10):
            current_date = start_date + timedelta(days=random.randint(0, 60))
            cust = random.choice(customers)
            pay = random.choice(payments)

            # 1. Retail Crop Sales
            crop = random.choice(crop_names)
            qty = Decimal(random.uniform(10.0, 500.0)).quantize(Decimal('0.00'))
            unit_price = Decimal(random.uniform(20.0, 150.0)).quantize(Decimal('0.00'))
            Retail_Crop_Sales.objects.create(
                user=user,
                Date=current_date,
                Crop_Name=crop,
                Quantity_Sold=qty,
                Unit_Price=unit_price,
                Customer_Name=cust,
                Payment_Method=pay
            )

            # 2. Retail Egg Sales
            tray = random.randint(0, 50)
            egg = random.randint(0, 30)
            if tray == 0 and egg == 0: tray = 1
            Retail_Egg_Sales.objects.create(
                user=user,
                Date=current_date,
                Tray_Count=tray,
                Egg_Count=egg,
                Price_Per_Tray=Decimal('180.00'),
                Price_Per_Egg=Decimal('7.00'),
                Customer_Name=random.choice(customers),
                Payment_Method=random.choice(payments)
            )

            # 3. Retail Milk Sales
            liters = Decimal(random.uniform(5.0, 100.0)).quantize(Decimal('0.00'))
            price_l = Decimal(random.choice(milk_prices))
            Retail_Milk_Sales.objects.create(
                user=user,
                Date=current_date,
                Quantity_Liters=liters,
                Price_Per_Liter=price_l,
                Customer_Name=random.choice(customers),
                Payment_Method=random.choice(payments)
            )

            # 4. Retail Machinery Renting
            mach = random.choice(machinery)
            serv = random.choice(services)
            hrs = Decimal(random.uniform(1.0, 12.0)).quantize(Decimal('0.00'))
            rate = Decimal(random.uniform(500.0, 1500.0)).quantize(Decimal('0.00'))
            Retail_Machinery_Renting.objects.create(
                user=user,
                Date=current_date,
                Machinery_Used=mach,
                Service_Provided=serv,
                Hours_Rented=hrs,
                Rate_Per_Hour=rate,
                Customer_Name=random.choice(customers),
                Payment_Method=random.choice(payments)
            )

            # 5. Retail Livestock Sales
            try:
                animal_type, breed = random.choice(livestock)
                qty_livestock = random.randint(1, 5)
                unit_price_livestock = Decimal(random.uniform(5000.0, 80000.0)).quantize(Decimal('0.00'))
                Retail_Livestock_Sales.objects.create(
                    user=user,
                    Date=current_date,
                    Animal_Type=animal_type,
                    Breed=breed,
                    Quantity_Sold=qty_livestock,
                    Unit_Price=unit_price_livestock,
                    Customer_Name=random.choice(customers),
                    Payment_Method=random.choice(payments)
                )
                records_count += 5
            except Exception:
                records_count += 4

    print(f"Successfully generated {records_count} Retail Operation records!")

if __name__ == "__main__":
    generate_retail_data()
