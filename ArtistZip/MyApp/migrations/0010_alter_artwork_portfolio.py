# Generated by Django 5.0.7 on 2024-07-24 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0009_rename_art_title_artwork_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='portfolio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artworks', to='MyApp.portfolio'),
        ),
    ]
