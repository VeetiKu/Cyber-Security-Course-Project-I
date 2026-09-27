from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ExpenseForm
from .models import Expense
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


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
    
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("expense_list")
    else:
        form = UserCreationForm()

    return render(request,
                  "registration/register.html",
                  {"form": form},)
    
@login_required
def expense_detail(request, expense_id):
    # FLAW 1 OWASP 2021 A01: Broken Access Control
    # The expense is retrieved without checking its owner.
    expense = get_object_or_404(Expense, pk=expense_id)

    # FIX:
    # expense = get_object_or_404(
    #     Expense,
    #     pk=expense_id,
    #     owner=request.user,)

    return render(
        request,
        "expenses/expense_detail.html",
        {"expense": expense},)