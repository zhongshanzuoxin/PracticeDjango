# Generated by Django 5.0.2 on 2024-02-25 20:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec_site', '0002_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ec_site.payment'),
        ),
    ]
