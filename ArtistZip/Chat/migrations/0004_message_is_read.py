# Generated by Django 5.0.6 on 2024-07-19 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0003_remove_message_is_read_alter_chatroom_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
