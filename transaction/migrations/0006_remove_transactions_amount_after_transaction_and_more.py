# Generated by Django 5.0.6 on 2024-09-16 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0005_alter_transactions_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='amount_after_transaction',
        ),
        migrations.AlterField(
            model_name='transactions',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True),
        ),
    ]
