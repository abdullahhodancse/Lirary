# Generated by Django 5.0.6 on 2024-09-17 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowbooks',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
    ]
