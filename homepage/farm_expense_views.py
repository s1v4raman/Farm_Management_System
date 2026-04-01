from django.shortcuts import render, redirect, get_object_or_404
from .models import FarmExpense
from .farm_expense_form import FarmExpenseForm

def show_farm_expenses(request):
    expenses = FarmExpense.objects.filter(user=request.user)
    return render(request, "homepage/show_farm_expenses.html", {"expenses": expenses})

def add_farm_expense(request):
    if request.method == "POST":
        form = FarmExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("homepage:show-farm-expenses")
    else:
        form = FarmExpenseForm()
    return render(request, "homepage/add_farm_expense.html", {"form": form})

def update_farm_expense(request, id):
    expense = get_object_or_404(FarmExpense, id=id, user=request.user)
    if request.method == "POST":
        form = FarmExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("homepage:show-farm-expenses")
    else:
        form = FarmExpenseForm(instance=expense)
    return render(request, "homepage/update_farm_expense.html", {"form": form, "expense": expense})

def delete_farm_expense(request, id):
    expense = get_object_or_404(FarmExpense, id=id, user=request.user)
    if request.method == "POST":
        expense.delete()
        return redirect("homepage:show-farm-expenses")
    return render(request, "homepage/delete_farm_expense.html", {"expense": expense})
