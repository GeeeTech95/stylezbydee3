# Generated by Django 4.2.15 on 2024-11-08 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0012_bespokeorder_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bespokeorder',
            name='order_id',
            field=models.CharField(default='3', editable=False, max_length=8, unique=True),
            preserve_default=False,
        ),
    ]
