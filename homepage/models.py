from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from decimal import Decimal
from django.core.validators import MaxValueValidator,MinValueValidator # type: ignore

# Create your models here.


class Employees(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    Eid = models.IntegerField(primary_key=True, default=0)
    Name = models.CharField(max_length=50)
    Country_code = models.CharField(max_length=4)
    Phone_number = models.CharField(max_length=9)
    Position = models.CharField(max_length=10)
    Salary = models.IntegerField()
    Performance = models.CharField(max_length=10)

    class Meta:
        db_table = "employees"


class Crops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    Cid = models.IntegerField(primary_key=True, default=0)
    Field_name = models.CharField(max_length=50)
    Field_description = models.TextField()
    Crop_name = models.CharField(max_length=50)
    Variety = models.CharField(max_length=20)
    Planting_date = models.DateField()
    Is_harvested = models.BooleanField(default=False)
    Harvesting_date = models.DateField(null=True, blank=True)

    def calculate_profit(self):
        if self.Harvesting_date and self.Sales:
            expenses_total = self.Expenses
            return self.Sales - expenses_total
        else:
            return None
        
class Crop_expenses(models.Model):
    crops=models.ForeignKey(Crops,on_delete=models.CASCADE)

    Expense_date=models.DateField(help_text='m/d/y')
    Expense_type=models.CharField(max_length=100)
    Expense_description=models.TextField()

    Expense_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    Supplier=models.CharField(max_length=255)
    Payment_method=models.CharField(max_length=50)
    Receipt_number=models.CharField(max_length=100)

    class Meta:
        db_table="Crop_expenses"


class Crop_sales(models.Model):
    crops=models.ForeignKey(Crops,on_delete=models.CASCADE)

    Sale_date=models.DateField(help_text='m/d/y')
    Quantity_sold=models.CharField(max_length=20)
    Unit_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    Total_price=models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    Buyer_information=models.TextField()
    Payment_method=models.CharField(max_length=20)
    Payment_status=models.CharField(max_length=20, choices=[('pending', 'Pending'), ('received', 'Received')])
    Invoice_number=models.CharField(max_length=20)
    Additional_notes=models.TextField(blank=True)


#lets over ride the save method in order before saving it calculates the total amount


    def save(self, *args, **kwargs):
        import re
        from decimal import Decimal
        
        try:
            qty_str = str(self.Quantity_sold)
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", qty_str)
            if numbers:
                quantity_sold = Decimal(numbers[0])
            else:
                quantity_sold = Decimal('0')
        except Exception:
            quantity_sold = Decimal('0')

        try:
            unit_price = Decimal(str(self.Unit_price))
        except Exception:
            unit_price = Decimal('0')

        self.Total_price = quantity_sold * unit_price
        super().save(*args, **kwargs)


class Machinery(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    
    Number_plate= models.CharField(max_length=20, primary_key=True)
    Equipment_name= models.CharField(max_length=20)
    Purchase_price= models.DecimalField(max_digits=10,decimal_places=2, default=0)
    Purchase_date = models.DateField()
    Operation=models.TextField(blank=True)

    class Meta:
        db_table = "Machinery"

class Machinery_activities(models.Model):
    machinery= models.ForeignKey(Machinery,on_delete=models.CASCADE)

    Activity_date=models.DateField(help_text="m/d/y")
    Activity_type=models.CharField(max_length=20)
    Activity_cost=models.IntegerField(blank=True)
    Description=models.TextField(blank=True)

    class meta:
        db_table="Machinery_activities"

class Machinery_maintenance(models.Model):
    machinery=models.ForeignKey(Machinery,on_delete=models.CASCADE)

    Date= models.DateField(help_text="m/d/y")
    Machinery_part=models.CharField(max_length=100)
    Technician_details=models.CharField(max_length=100,blank="True")
    Cost= models.IntegerField()
    Description=models.TextField()

    class Meta:
        db_table="Machinery_activities"


# Livestock Models Removed

class Milk_production(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, default=1)


    Year=models.IntegerField(validators=[MinValueValidator(1)])
    Month=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    Day=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)],default=1)

    Livestock_number=models.IntegerField()
    Morning_production=models.DecimalField(max_digits=10,decimal_places=2,help_text='production in litres')
    Midday_production=models.DecimalField(max_digits=10,decimal_places=2,help_text='production in litres', blank=True)
    Evening_production=models.DecimalField(max_digits=10,decimal_places=2,help_text='production in litres',blank=True)
    Total_production=models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)

    Morning_consumption=models.DecimalField(max_digits=10,decimal_places=2,help_text='feed consumed in kg')
    Evening_consumption=models.DecimalField(max_digits=10,decimal_places=2,help_text='feed consumed in kg',blank=True)
    Total_consumption=models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)

    def save(self,*args,**kwargs):
        morning_production=float(self.Morning_production)
        midday_production=float(self.Midday_production)
        evening_production=float(self.Evening_production)

        self.Total_production=Decimal(morning_production+midday_production+evening_production)

        morning_consumption=float(self.Morning_consumption)
        evening_consumption=float(self.Evening_consumption)

        self.Total_consumption=Decimal(morning_consumption+evening_consumption)

        super().save(*args,**kwargs)


class Eggs_production(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, default=1)

    Year =models.IntegerField(validators=[MinValueValidator(1)])
    Month = models.IntegerField(validators= [MinValueValidator(1), MaxValueValidator(12)])
    Day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    Poultry_number=models.IntegerField()

    Morning_egg_collection=models.DecimalField(max_digits=10,decimal_places=2,help_text='total number of eggs collected')
    Midday_egg_collection=models.DecimalField(max_digits=10,decimal_places=2,help_text='total number of eggs collected', blank=True)
    Evening_egg_collection=models.DecimalField(max_digits=10,decimal_places=2,help_text='total number of eggs collected',blank=True)
    Total_egg_collection=models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)

    Morning_feeds=models.DecimalField(max_digits=10,decimal_places=2,help_text='feed consumed in kg')
    Evening_feeds=models.DecimalField(max_digits=10,decimal_places=2,help_text='feed consumed in kg',blank=True)
    Total_feeds=models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    Comments=models.TextField(null=True,blank=True)

    def save(self,*args, **kwargs):
        morning_egg_collection=float(self.Morning_egg_collection)
        midday_egg_collection=float(self.Midday_egg_collection)
        evening_egg_collection=float(self.Evening_egg_collection)

        self.Total_egg_collection=Decimal(morning_egg_collection+midday_egg_collection+evening_egg_collection)

        morning_feeds=float(self.Morning_feeds)
        evening_feeds=float(self.Evening_feeds)
        self.Total_feeds=Decimal(morning_feeds+evening_feeds)
        
        super().save(*args, **kwargs)

class FarmExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    Expense_date = models.DateField(help_text='m/d/y')
    Season_or_crop = models.CharField(max_length=50, help_text='e.g., Wheat 2026')
    Seed_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Fertilizer_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Other_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    Crop_sale = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Income from crop sale")
    
    Total_investment = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    Profit = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)

    class Meta:
        db_table = "FarmExpense"

    def save(self, *args, **kwargs):
        # Calculate total investment
        self.Total_investment = Decimal(float(self.Seed_cost) + float(self.Fertilizer_cost) + float(self.Labor_cost) + float(self.Other_costs))
        
        # Calculate profit
        self.Profit = Decimal(float(self.Crop_sale) - float(self.Total_investment))
        
        super().save(*args, **kwargs)

class WaterSchedule(models.Model):
    WATER_LEVEL_CHOICES = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Dry', 'Dry'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    crop = models.CharField(max_length=100, help_text='Select crop type for water estimation')
    field_area = models.DecimalField(max_digits=8, decimal_places=2, help_text='Area in Acres')
    water_level = models.CharField(max_length=20, choices=WATER_LEVEL_CHOICES, default='Dry', help_text='Current water level of the land')
    water_source_flow_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text='Pump flow rate in Liters per Minute (LPM)')
    mobile_number = models.CharField(max_length=15, default="", help_text='Phone number to send SMS alert to (e.g. +919876543210)')

    
    calculated_time_minutes = models.IntegerField(default=0, editable=False)
    
    status = models.CharField(max_length=20, default='Pending') # Pending, Flowing, Completed
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "WaterSchedule"

# --- RETAIL OPERATIONS MODELS ---

class Retail_Crop_Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Date = models.DateField(help_text='m/d/y')
    Crop_Name = models.CharField(max_length=50)
    Quantity_Sold = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity in Kg/Tons")
    Unit_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Total_Amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    Customer_Name = models.CharField(max_length=100)
    Payment_Method = models.CharField(max_length=20, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('UPI', 'UPI'), ('Other', 'Other')])
    Product_Image = models.ImageField(upload_to='retail_images/', null=True, blank=True)

    class Meta:
        db_table = "Retail_Crop_Sales"

    def save(self, *args, **kwargs):
        self.Total_Amount = Decimal(float(self.Quantity_Sold) * float(self.Unit_Price))
        super().save(*args, **kwargs)

class Retail_Egg_Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Date = models.DateField(help_text='m/d/y')
    Tray_Count = models.IntegerField(default=0, help_text="Number of trays sold")
    Egg_Count = models.IntegerField(default=0, help_text="Number of individual eggs sold")
    Price_Per_Tray = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Price_Per_Egg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Total_Amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    Customer_Name = models.CharField(max_length=100)
    Payment_Method = models.CharField(max_length=20, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('UPI', 'UPI'), ('Other', 'Other')], default='Cash')
    Product_Image = models.ImageField(upload_to='retail_images/', null=True, blank=True)

    class Meta:
        db_table = "Retail_Egg_Sales"

    def save(self, *args, **kwargs):
        tray_total = float(self.Tray_Count) * float(self.Price_Per_Tray)
        egg_total = float(self.Egg_Count) * float(self.Price_Per_Egg)
        self.Total_Amount = Decimal(tray_total + egg_total)
        super().save(*args, **kwargs)

class Retail_Milk_Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Date = models.DateField(help_text='m/d/y')
    Quantity_Liters = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity in Liters")
    Price_Per_Liter = models.DecimalField(max_digits=10, decimal_places=2)
    Total_Amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    Customer_Name = models.CharField(max_length=100)
    Payment_Method = models.CharField(max_length=20, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('UPI', 'UPI'), ('Other', 'Other')], default='Cash')
    Product_Image = models.ImageField(upload_to='retail_images/', null=True, blank=True)

    class Meta:
        db_table = "Retail_Milk_Sales"

    def save(self, *args, **kwargs):
        self.Total_Amount = Decimal(float(self.Quantity_Liters) * float(self.Price_Per_Liter))
        super().save(*args, **kwargs)

class Retail_Machinery_Renting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Date = models.DateField(help_text='m/d/y')
    Machinery_Used = models.CharField(max_length=100)
    Service_Provided = models.CharField(max_length=100)
    Hours_Rented = models.DecimalField(max_digits=6, decimal_places=2)
    Rate_Per_Hour = models.DecimalField(max_digits=10, decimal_places=2)
    Total_Amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    Customer_Name = models.CharField(max_length=100)
    Payment_Method = models.CharField(max_length=20, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('UPI', 'UPI'), ('Other', 'Other')], default='Cash')
    Product_Image = models.ImageField(upload_to='retail_images/', null=True, blank=True)

    class Meta:
        db_table = "Retail_Machinery_Renting"

    def save(self, *args, **kwargs):
        self.Total_Amount = Decimal(float(self.Hours_Rented) * float(self.Rate_Per_Hour))
        super().save(*args, **kwargs)

# Retail Livestock Sales Model Removed

class ContactDetail(models.Model):
    phone = models.CharField(max_length=20, default="+91 91594 42229")
    email = models.EmailField(default="support@agrimarket.com")
    address = models.TextField(default="#42, Madurai Bypass Rd, Madurai, TN 625020")
    
    class Meta:
        verbose_name = "Contact Detail"
        verbose_name_plural = "Contact Details"

    def __str__(self):
        return "System Contact Information"
