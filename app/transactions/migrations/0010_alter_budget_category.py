# Generated by Django 5.0.7 on 2024-07-15 17:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0009_remove_transaction_date_remove_transfer_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.category'),
        ),
    ]
