from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ExpenseForm
from .models import Expense


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(owner=request.user).order_by("-date")
    return render(request,
        "expenses/expense_list.html",
        {"expenses": expenses},)


@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.owner = request.user
            expense.save()
            return redirect("expense_list")
    else:
        form =ExpenseForm()

    return render(request,
        "expenses/expense_form.html",
        {"form": form},)