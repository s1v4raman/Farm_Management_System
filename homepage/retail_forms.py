from django import forms  # type: ignore
from .models import Retail_Crop_Sales, Retail_Egg_Sales, Retail_Milk_Sales, Retail_Machinery_Renting  # type: ignore

class RetailCropSalesForm(forms.ModelForm):
    class Meta:
        model = Retail_Crop_Sales
        fields = [
            'Date',
            'Crop_Name',
            'Quantity_Sold',
            'Unit_Price',
            'Payment_Method',
            'Product_Image'
        ]
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'})
        }

class RetailEggSalesForm(forms.ModelForm):
    class Meta:
        model = Retail_Egg_Sales
        fields = [
            'Date',
            'Tray_Count',
            'Egg_Count',
            'Price_Per_Tray',
            'Price_Per_Egg',
            'Payment_Method',
            'Product_Image'
        ]
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'})
        }

class RetailMilkSalesForm(forms.ModelForm):
    class Meta:
        model = Retail_Milk_Sales
        fields = [
            'Date',
            'Quantity_Liters',
            'Price_Per_Liter',
            'Payment_Method',
            'Product_Image'
        ]
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'})
        }

class RetailMachineryRentingForm(forms.ModelForm):
    class Meta:
        model = Retail_Machinery_Renting
        fields = [
            'Date',
            'Machinery_Used',
            'Service_Provided',
            'Hours_Rented',
            'Rate_Per_Hour',
            'Payment_Method',
            'Product_Image'
        ]
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'})
        }

# Retail Livestock Sales Form Removed
