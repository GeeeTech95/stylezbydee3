# Generated by Django 3.2.12 on 2023-11-23 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_remove_product_is_available_on_preorder'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartLineAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='cart.cartline', verbose_name='Line')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.productattribute', verbose_name='Option')),
            ],
            options={
                'verbose_name': 'Line attribute',
                'verbose_name_plural': 'Line attributes',
            },
        ),
    ]
