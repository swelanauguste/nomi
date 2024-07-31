from django.urls import path

from . import views

urlpatterns = [
    path("", views.accounts, name="accounts"),
    path("accounts/add/", views.add_account, name="add_account"),
    path("account/<int:account_id>/", views.account_detail, name="account_detail"),
    path("transactions/add/", views.add_transaction, name="add_transaction"),
    path(
        "transaction/update/<int:transaction_id>/",
        views.update_transaction,
        name="update_transaction",
    ),
    path("transactions/view/", views.view_transactions, name="view_transactions"),
    path("budgets/", views.budget_list, name="budget_list"),
    path("budgets/add/", views.budget_create, name="add_budget"),
    path(
        "recurring_transactions/",
        views.recurring_transactions,
        name="recurring_transactions",
    ),
    path(
        "recurring_transactions/add/",
        views.add_recurring_transaction,
        name="add_recurring_transaction",
    ),
    path("transfer/", views.add_transfer, name="transfer"),
    path("add_category/", views.add_category, name="add_category"),
    path("get_categories/", views.get_categories, name="get_categories"),
    path("add_rule/", views.add_rule, name="add_rule"),
    path("get_rules/", views.get_rules, name="get_rules"),
]
