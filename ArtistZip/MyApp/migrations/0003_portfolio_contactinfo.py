# Generated by Django 5.0.6 on 2024-07-22 12:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0002_remove_artwork_artist_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=255, verbose_name='작가명')),
                ('art_title', models.CharField(max_length=255, verbose_name='작품 제목')),
                ('art_description', models.TextField(verbose_name='작품 설명')),
            ],
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram', models.URLField(blank=True, verbose_name='Instagram')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='이메일')),
                ('homepage', models.URLField(blank=True, verbose_name='홈페이지')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
