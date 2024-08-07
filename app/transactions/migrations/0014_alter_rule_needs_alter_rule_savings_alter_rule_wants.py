# Generated by Django 5.0.7 on 2024-07-19 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0013_rename_living_rule_needs_alter_budget_rule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='needs',
            field=models.PositiveIntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='rule',
            name='savings',
            field=models.PositiveIntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='rule',
            name='wants',
            field=models.PositiveIntegerField(default=30),
        ),
    ]
