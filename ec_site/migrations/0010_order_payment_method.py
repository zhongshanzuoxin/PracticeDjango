# Generated by Django 5.0.2 on 2024-03-12 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec_site', '0009_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
