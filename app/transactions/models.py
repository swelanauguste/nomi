import decimal

from django.db import models
from django.utils import timezone
from users.models import User


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ${self.balance}"


class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_account = models.ForeignKey(
        Account, related_name="transfer_from", on_delete=models.CASCADE
    )
    to_account = models.ForeignKey(
        Account, related_name="transfer_to", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.from_account != self.to_account:
            if self.from_account.balance >= self.amount:
                self.from_account.balance -= self.amount
                self.to_account.balance += self.amount
                self.from_account.save()
                self.to_account.save()
                super().save(*args, **kwargs)
            else:
                raise ValueError("Insufficient funds in the source account.")
        else:
            raise ValueError("Cannot transfer to the same account.")


class Category(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_categories"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_transactions"
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        help_text='<span class="text-primary" style="cursor: pointer;" onclick="openAddCategoryWindow()">add category</span>',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    TRANSACTION_TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
        ("savings", "Savings"),
    ]
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)

    def save(self, *args, **kwargs):
        # Get the original transaction if it exists
        if self.pk:
            original = Transaction.objects.get(pk=self.pk)
            if original.transaction_type == "income":
                self.account.balance -= original.amount
            elif original.transaction_type == "expense":
                self.account.balance += original.amount

        if self.transaction_type == "income":
            self.account.balance += self.amount
        elif self.transaction_type == "expense":
            self.account.balance -= self.amount

        self.account.save()
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_date} - {self.transaction_type} - {self.amount}"


class Rule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    savings = models.PositiveIntegerField(default=20)
    wants = models.PositiveIntegerField(default=30)
    needs = models.PositiveIntegerField(default=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.savings}-{self.wants}-{self.needs}"


class Budget(models.Model):
    add_rule = '<span class="text-primary" style="cursor: pointer;" onclick="openAddRuleWindow()">add rule</span>'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rule = models.ForeignKey(
        Rule, on_delete=models.CASCADE, null=True, help_text=add_rule
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # MONTH_CHOICES = [
    #     ("01", "January"),
    #     ("02", "February"),
    #     ("03", "March"),
    #     ("04", "April"),
    #     ("05", "May"),
    #     ("06", "June"),
    #     ("07", "July"),
    #     ("08", "August"),
    #     ("09", "September"),
    #     ("10", "October"),
    #     ("11", "November"),
    #     ("12", "December"),
    # ]
    # month = models.CharField(max_length=2, choices=MONTH_CHOICES, null=True, blank=True)

    # The 70-20-10 budget formula divides your after-tax income into three buckets: 70% for living expenses, 20% for savings and debt, and 10% for additional savings and donations.

    # One of the most common types of percentage-based budgets is the 50/30/20 rule. The idea is to divide your income into three categories, spending 50% on needs, 30% on wants, and 20% on savings.

    # The 40/40/20 rule comes in during the saving phase of his wealth creation formula. Cardone says that from your gross income, 40% should be set aside for taxes, 40% should be saved, and you should live off of the remaining 20%.

    class Meta:
        ordering = ["-pk"]

    def get_savings(self):
        if self.rule:
            return round(self.amount * decimal.Decimal(self.rule.savings / 100), 2)
        return None

    def get_needs(self):
        if self.rule:
            return round(self.amount * decimal.Decimal(self.rule.needs / 100), 2)
        return None

    def get_wants(self):
        if self.rule:
            return round(self.amount * decimal.Decimal(self.rule.wants / 100), 2)
        return None

    def __str__(self):
        return f"${self.amount}"


class RecurringTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    INTERVAL_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    interval = models.CharField(
        max_length=10,
        choices=INTERVAL_CHOICES,
        help_text="e.g., daily, weekly, monthly",
    )  # e.g., 'daily', 'weekly', 'monthly'
    next_occurrence = models.DateField()

    def __str__(self):
        return f"${self.amount} {self.interval}"
