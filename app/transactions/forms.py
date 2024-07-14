from django import forms

from .models import Account, Budget, Category, RecurringTransaction, Transaction


class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all())
    to_account = forms.ModelChoiceField(queryset=Account.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(TransferForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["from_account"].queryset = Account.objects.filter(user=user)
            self.fields["to_account"].queryset = Account.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        from_account = cleaned_data.get("from_account")
        to_account = cleaned_data.get("to_account")
        if from_account and to_account and from_account == to_account:
            raise forms.ValidationError(
                "From account and to account cannot be the same."
            )
        return cleaned_data


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["category", "amount", "month"]


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
            "description",
            "transaction_date",
            "transaction_type",
        ]

        widgets = {
            "transaction_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": "3"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
