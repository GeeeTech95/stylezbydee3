# Generated by Django 4.2.15 on 2024-11-20 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_user_access_level'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='access_level',
            new_name='access_permission_level',
        ),
    ]
