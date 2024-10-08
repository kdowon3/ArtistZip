# Generated by Django 5.0.6 on 2024-08-17 05:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0005_portfolio_background_color'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Special_Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='special_portfolio_images/', verbose_name='스페셜 포트폴리오 이미지')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special_portfolios', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
