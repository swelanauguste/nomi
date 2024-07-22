# Generated by Django 5.0.7 on 2024-07-22 04:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0017_remove_rule_name_alter_rule_needs_alter_rule_savings_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='transfer',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('income', 'Income'), ('expense', 'Expense')], max_length=7),
        ),
    ]
