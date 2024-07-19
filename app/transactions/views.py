import datetime
from itertools import chain
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AccountForm,
    BudgetForm,
    CategoryForm,
    RecurringTransactionForm,
    RuleForm,
    TransactionFilterForm,
    TransactionForm,
    TransferForm,
)
from .models import (
    Account,
    Budget,
    Category,
    RecurringTransaction,
    Rule,
    Transaction,
    Transfer,
)


@login_required
def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    transactions = Transaction.objects.filter(account=account)
    from_transfers = Transfer.objects.filter(from_account=account)
    to_transfers = Transfer.objects.filter(to_account=account)

    # Add a date attribute to all items for sorting
    transactions = list(transactions)
    for t in transactions:
        t.date = t.created_at

    from_transfers = list(from_transfers)
    for ft in from_transfers:
        ft.date = ft.created_at
        ft.type = "from_transfer"

    to_transfers = list(to_transfers)
    for tt in to_transfers:
        tt.date = tt.created_at
        tt.type = "to_transfer"

    # Combine and sort by date
    combined_transactions = list(chain(transactions, from_transfers, to_transfers))
    combined_transactions.sort(
        key=lambda x: (
            x.created_at
            if isinstance(x.created_at, datetime.datetime)
            else datetime.datetime.combine(x.created_at, datetime.time.min)
        ),
        reverse=True,
    )

    return render(
        request,
        "accounts/account_detail.html",
        {"account": account, "transactions": combined_transactions},
    )


@login_required
def get_rules(request):
    rules = Rule.objects.filter(user=request.user).values("id", "name")
    return JsonResponse({"rules": list(rules)})


@login_required
def add_rule(request):
    if request.method == "POST":
        form = RuleForm(request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.user = request.user
            rule.save()
            return render(
                request, "transactions/close_window.html"
            )  # Template to close the window after adding the rule
    else:
        form = RuleForm()
    return render(request, "transactions/add_rule.html", {"form": form})


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
def add_transfer(request):
    if request.method == "POST":
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                form.save(commit=False).user = request.user
                form.save()
                return redirect("accounts")  # Replace with your desired redirect URL
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = TransferForm(user=request.user)
    return render(request, "transactions/transfer.html", {"form": form})


@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, "budgets/budget_list.html", {"budgets": budgets})


@login_required
def budget_create(request):
    if request.method == "POST":
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect("budget_list")
    else:
        form = BudgetForm(user=request.user)
    return render(request, "budgets/budget_form.html", {"form": form})


@login_required
def budget_edit(request, budget_id):
    budget = Budget.objects.get(id=budget_id, user=request.user)
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("budget_list")
    else:
        form = BudgetForm(instance=budget, user=request.user)
    return render(request, "budgets/budget_form.html", {"form": form})


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
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect(
                "views_transactions"
            )  # Change to your transaction list view name
    else:
        form = TransactionForm(user=request.user)
    return render(request, "transactions/add_transaction.html", {"form": form})
