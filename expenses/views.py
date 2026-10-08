from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ExpenseForm
from .models import Expense
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
import logging

logger = logging.getLogger(__name__)

@login_required
def expense_list(request):
    search = request.GET.get("q", "")

    # FLAW 3 OWASP 2021 A03: Injection
    # User input is inserted directly into an SQL statement.
    sql = f"SELECT * FROM expenses_expense WHERE owner_id = {request.user.id} AND title LIKE '%{search}%' ORDER BY date DESC"
    expenses = Expense.objects.raw(sql)

    # FIX: Pass the values separately to the query to avoid injection.
    # sql = """SELECT * FROM expenses_expense WHERE owner_id = %s AND title LIKE %s ORDER BY date DESC"""
    # expenses = Expense.objects.raw(sql,[request.user.id, f"%{search}%"],)

    return render(request, "expenses/expense_list.html",{"expenses":expenses,"search":search,},)


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

            # FLAW 2 OWASP 2021 A02: Cryptographic Failure
            # The password is stored without hashing or encryption in passwords.txt.
            with open("passwords.txt", "a",
                encoding="utf-8",) as password_file:
                password_file.write(
                    f"{user.username}: "
                    f"{form.cleaned_data['password1']}\n")     
            # FIX:
            # Remove the block above (lines 56-60). Django already stores the password using secure hashing.

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
    
@login_required
@require_POST
def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id, owner=request.user,)

    # FLAW 5 OWASP 2021 A09: Security Logging and Monitoring Failures
    # The application deletes an expense without recording who performed the sensitive action or which expense was deleted.
    expense.delete()
    
    # FIX:
    # logger.warning("User %s deleted expense %s", request.user.username, expense_id,)
    return redirect("expense_list")