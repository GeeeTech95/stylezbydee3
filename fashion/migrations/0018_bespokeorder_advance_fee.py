# Generated by Django 4.2.15 on 2024-11-16 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0017_bespokeorderstaffinfo_date_staff_is_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bespokeorder',
            name='advance_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
    ]
