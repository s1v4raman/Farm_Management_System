from django import forms
from .models import Employees


class EmployeesForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = [
            "Eid",
            "Name",
            "Country_code",
            "Phone_number",
            "Position",
            "Salary",
            "Performance",
        ]

class EmployeesCreationForm(EmployeesForm):
    employee_username = forms.CharField(max_length=150, required=True, help_text="New Employee Login Username")
    employee_password = forms.CharField(widget=forms.PasswordInput, required=True, help_text="New Employee Login Password")

    class Meta(EmployeesForm.Meta):
        fields = [
            "Eid",
            "employee_username",
            "employee_password",
            "Name",
            "Country_code",
            "Phone_number",
            "Position",
            "Salary",
            "Performance",
        ]

class EmployeesUpdateForm(EmployeesForm):
    employee_username = forms.CharField(max_length=150, required=True, help_text="Employee Login Username")
    employee_password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep current password")

    class Meta(EmployeesForm.Meta):
        fields = [
            "Eid",
            "employee_username",
            "employee_password",
            "Name",
            "Country_code",
            "Phone_number",
            "Position",
            "Salary",
            "Performance",
        ]
