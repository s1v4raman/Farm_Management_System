from django import forms # type: ignore
from .models import Crops,Crop_expenses,Crop_sales # type: ignore


class CropsForm(forms.ModelForm):
    class Meta:
        model = Crops
        fields = [
            "Cid",
            "Field_name",
            "Field_description",
            "Crop_name",
            "Variety",
            "Planting_date",
            "Harvesting_date",
        ]
        widgets = {
            'Planting_date': forms.DateInput(attrs={'type': 'date'}),
            'Harvesting_date': forms.DateInput(attrs={'type': 'date'}),
        }

class Crop_expensesForm(forms.ModelForm):
    class Meta:
        model=Crop_expenses
        fields=[
            "Expense_date",
            "Expense_type",
            "Expense_description",
            "Expense_amount",
            "Supplier",
            "Payment_method",
            "Receipt_number"
        ]
        widgets = {
            'Expense_date': forms.DateInput(attrs={'type': 'date'}),
        }

class Crop_salesForm(forms.ModelForm):
    class Meta:
        model=Crop_sales
        fields=[
            'Sale_date',
            'Quantity_sold',
            'Unit_price',
            'Buyer_information',
            'Payment_method',
            'Payment_status',
            'Invoice_number',
            'Additional_notes'
        ]
        widgets = {
            'Sale_date': forms.DateInput(attrs={'type': 'date'}),
        }
