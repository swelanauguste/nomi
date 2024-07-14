from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone



from .forms import (
    AccountForm,
    BudgetForm,
    CategoryForm,
    RecurringTransactionForm,
    TransactionFilterForm,
    TransactionForm,
    TransferForm,
)
from .models import Account, Budget, Category, RecurringTransaction, Transaction


@login_required
def get_categories(request):
    categories = Category.objects.filter(user=request.user).values("id", "name")
    return JsonResponse({"categories": list(categories)})


@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return render(
                request, "transactions/close_window.html"
            )  # Template to close the window after adding the category
    else:
        form = CategoryForm()
    return render(request, "transactions/add_category.html", {"form": form})


@login_required
def transfer(request):
    if request.method == "POST":
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            from_account = form.cleaned_data["from_account"]
            to_account = form.cleaned_data["to_account"]
            amount = form.cleaned_data["amount"]

            if from_account.balance >= amount:
                # Use a default category for transfers
                transfer_category, created = Category.objects.get_or_create(
                    name="Transfer", defaults={"user": request.user}
                )
                # Create transaction for from_account (Debit)
                Transaction.objects.create(
                    user=request.user,
                    account=from_account,
                    category=transfer_category,
                    # You can assign a specific category if needed
                    amount=amount,
                    description=f"Transfer to {to_account.name}",
                    transaction_date=timezone.now(),
                    transaction_type="expense",
                )

                # Create transaction for to_account (Credit)
                Transaction.objects.create(
                    user=request.user,
                    account=to_account,
                    category=transfer_category,
                    # You can assign a specific category if needed
                    amount=amount,
                    description=f"Transfer from {from_account.name}",
                    transaction_date=timezone.now(),
                    transaction_type="income",
                )

                return redirect("accounts")
            else:
                form.add_error("amount", "Insufficient funds in the source account.")
    else:
        form = TransferForm(user=request.user)
    return render(request, "transactions/transfer.html", {"form": form})


@login_required
def budgets(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, "transactions/budgets.html", {"budgets": budgets})


@login_required
def add_budget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect("budgets")
    else:
        form = BudgetForm()
    return render(request, "transactions/add_budget.html", {"form": form})


@login_required
def recurring_transactions(request):
    recurring_transactions = RecurringTransaction.objects.filter(user=request.user)
    return render(
        request,
        "transactions/recurring_transactions.html",
        {"recurring_transactions": recurring_transactions},
    )


@login_required
def add_recurring_transaction(request):
    if request.method == "POST":
        form = RecurringTransactionForm(request.POST)
        if form.is_valid():
            recurring_transaction = form.save(commit=False)
            recurring_transaction.user = request.user
            recurring_transaction.save()
            return redirect("recurring_transactions")
    else:
        form = RecurringTransactionForm()
    return render(
        request, "transactions/add_recurring_transaction.html", {"form": form}
    )


@login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(user=request.user)[:5]
    if request.method == "GET":
        form = TransactionFilterForm(request.GET)
        if form.is_valid():
            if form.cleaned_data["account"]:
                transactions = transactions.filter(account=form.cleaned_data["account"])
            if form.cleaned_data["category"]:
                transactions = transactions.filter(
                    category=form.cleaned_data["category"]
                )
            if form.cleaned_data["transaction_type"]:
                transactions = transactions.filter(
                    transaction_type=form.cleaned_data["transaction_type"]
                )
            if form.cleaned_data["start_date"]:
                transactions = transactions.filter(
                    transaction_date__gte=form.cleaned_data["start_date"]
                )
            if form.cleaned_data["end_date"]:
                transactions = transactions.filter(
                    transaction_date__lte=form.cleaned_data["end_date"]
                )
    else:
        form = TransactionFilterForm()

    return render(
        request,
        "transactions/view_transactions.html",
        {"form": form, "transactions": transactions},
    )


@login_required
def accounts(request):
    accounts = Account.objects.filter(user=request.user)
    total_balance = accounts.aggregate(total=models.Sum("balance"))["total"] or 0
    total_balance = round(total_balance, 2)
    return render(
        request,
        "transactions/accounts.html",
        {"accounts": accounts, "total_balance": total_balance},
    )


@login_required
def add_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect("accounts")
    else:
        form = AccountForm()
    return render(request, "transactions/add_account.html", {"form": form})


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("accounts")
    else:
        form = TransactionForm()
    categories = Category.objects.filter(user=request.user)
    return render(
        request,
        "transactions/add_transaction.html",
        {"form": form, "categories": categories},
    )
