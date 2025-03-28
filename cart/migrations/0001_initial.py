# Generated by Django 3.2.12 on 2023-11-14 20:26

import core.functions
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0007_remove_product_is_available_on_preorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Open', 'Open - currently active'), ('Saved', 'Saved - for items to be purchased later'), ('Frozen', 'Frozen - the cart cannot be modified'), ('Submitted', 'Submitted - has been ordered at the checkout')], default='Open', max_length=128, verbose_name='Status')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_submitted', models.DateTimeField(blank=True, null=True, verbose_name='Date submitted')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='CartLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_reference', models.SlugField(max_length=128, verbose_name='Line Reference')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('price_currency', models.CharField(default=core.functions.get_default_currency, max_length=12, verbose_name='Currency')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Price ')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date Updated')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='cart.cart', verbose_name='Cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_lines', to='shop.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Cart line',
                'verbose_name_plural': 'Cart lines',
                'ordering': ['date_created', 'pk'],
                'unique_together': {('cart', 'line_reference')},
            },
        ),
    ]
