from django import forms

from .models import (
    Account,
    Budget,
    Category,
    RecurringTransaction,
    Rule,
    Transaction,
    Transfer,
)


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ["from_account", "to_account", "amount", "date"]
        
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["from_account"].queryset = Account.objects.filter(user=user)
            self.fields["to_account"].queryset = Account.objects.filter(user=user)


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["amount", "rule"]
        widgets = {
            "amount": forms.NumberInput(attrs={"step": "0.01"}),
            "rule": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["rule"].queryset = Rule.objects.filter(user=user)


class RecurringTransactionForm(forms.ModelForm):
    class Meta:
        model = RecurringTransaction
        fields = [
            "account",
            "category",
            "amount",
            "description",
            "interval",
            "next_occurrence",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": "3"}),
            "next_occurrence": forms.DateInput(attrs={"type": "date"}),
        }


class TransactionFilterForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.all(), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    transaction_type = forms.ChoiceField(
        choices=Transaction.TRANSACTION_TYPE_CHOICES, required=False
    )
    start_date = forms.DateTimeField(
        required=False, widget=forms.DateTimeInput(attrs={"type": "date"})
    )
    end_date = forms.DateTimeField(
        required=False, widget=forms.DateTimeInput(attrs={"type": "date"})
    )


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "balance"]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "account",
            "category",
            "amount",
            "date",
            "description",
            "transaction_type",
        ]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": "3"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["account"].queryset = Account.objects.filter(user=user)
            self.fields["category"].queryset = Category.objects.filter(user=user)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "name",
        ]


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ["savings", "needs", "wants", "description"]

        widgets = {
            "description": forms.Textarea(attrs={"rows": "3"}),
        }
