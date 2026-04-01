from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from .models import FarmExpense  # type: ignore
from .farm_expense_form import FarmExpenseForm  # type: ignore

def show_farm_expenses(request):
    if request.user.is_superuser:
        expenses = FarmExpense.objects.all()
    else:
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
    if request.user.is_superuser:
        expense = get_object_or_404(FarmExpense, id=id)
    else:
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
    if request.user.is_superuser:
        expense = get_object_or_404(FarmExpense, id=id)
    else:
        expense = get_object_or_404(FarmExpense, id=id, user=request.user)
    if request.method == "POST":
        expense.delete()
        return redirect("homepage:show-farm-expenses")
    return render(request, "homepage/delete_farm_expense.html", {"expense": expense})
