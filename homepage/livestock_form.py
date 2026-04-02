from django import forms 
from .models import Milk_production, Eggs_production

class Milk_productionForm(forms.ModelForm):
    Record_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), help_text='Select the date of production')

    class Meta:
        model=Milk_production

        fields=[
            'Livestock_number',
            'Morning_production',
            'Midday_production',
            'Evening_production',
            'Morning_consumption',
            'Evening_consumption'
        ]

class Egg_productionForm(forms.ModelForm):
    Record_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), help_text='Select the date of collection')

    class Meta:
        model=Eggs_production

        fields=[
            'Poultry_number',
            'Morning_egg_collection',
            'Midday_egg_collection',
            'Evening_egg_collection',
            'Morning_feeds',
            'Evening_feeds',
            'Comments'
        ]