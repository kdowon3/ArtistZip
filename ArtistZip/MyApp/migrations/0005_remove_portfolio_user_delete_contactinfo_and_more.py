# Generated by Django 4.2.14 on 2024-07-24 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0004_portfolio_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='user',
        ),
        migrations.DeleteModel(
            name='ContactInfo',
        ),
        migrations.DeleteModel(
            name='Portfolio',
        ),
    ]
