# Generated by Django 5.0.4 on 2024-08-13 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
    ]
