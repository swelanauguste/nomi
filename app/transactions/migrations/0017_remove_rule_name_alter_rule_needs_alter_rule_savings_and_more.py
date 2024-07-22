# Generated by Django 5.0.7 on 2024-07-21 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0016_alter_budget_rule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rule',
            name='name',
        ),
        migrations.AlterField(
            model_name='rule',
            name='needs',
            field=models.PositiveIntegerField(default=30, help_text='%'),
        ),
        migrations.AlterField(
            model_name='rule',
            name='savings',
            field=models.PositiveIntegerField(default=30, help_text='%'),
        ),
        migrations.AlterField(
            model_name='rule',
            name='wants',
            field=models.PositiveIntegerField(default=30, help_text='%'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('income', 'Income'), ('expense', 'Expense'), ('savings', 'Savings')], max_length=7),
        ),
    ]