# Generated by Django 3.2.12 on 2023-11-23 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cartlineattribute'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartline',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='cartline',
            name='line_reference',
        ),
    ]
