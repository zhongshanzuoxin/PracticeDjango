# Generated by Django 5.0.2 on 2024-02-28 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec_site', '0005_alter_shippingaddress_address_line1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='recipient_name',
            field=models.CharField(default='田中', max_length=30, verbose_name='受取人名'),
            preserve_default=False,
        ),
    ]