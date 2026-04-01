from django import forms # type: ignore
from .models import FarmExpense # type: ignore

class FarmExpenseForm(forms.ModelForm):
    class Meta:
        model = FarmExpense
        fields = [
            'Expense_date',
            'Season_or_crop',
            'Seed_cost',
            'Fertilizer_cost',
            'Labor_cost',
            'Other_costs',
            'Crop_sale',
        ]
