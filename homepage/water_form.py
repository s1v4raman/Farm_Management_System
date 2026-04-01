from django import forms # type: ignore
from .models import WaterSchedule # type: ignore
from .utils.water_calc import CROP_CHOICES

class WaterScheduleForm(forms.ModelForm):
    crop = forms.ChoiceField(choices=CROP_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = WaterSchedule
        fields = ['crop', 'field_area', 'water_source_flow_rate', 'mobile_number']
        widgets = {
            'field_area': forms.NumberInput(attrs={'placeholder': 'e.g., 2.5', 'step': '0.1'}),
            'water_source_flow_rate': forms.NumberInput(attrs={'placeholder': 'e.g., 500', 'step': '10'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': '+919876543210', 'type': 'tel'}),
        }
