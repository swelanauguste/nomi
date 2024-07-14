from django.db import models
from users.models import User


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ${self.balance}"


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
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    TRANSACTION_TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
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


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(null=True)

    def __str__(self):
        return f"${self.amount} - {self.start_date} to {self.end_date}"


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
