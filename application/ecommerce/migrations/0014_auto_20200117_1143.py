# Generated by Django 3.0.1 on 2020-01-17 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0013_auto_20200117_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venteticket',
            name='promo',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='venteticket',
            name='promo_client',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='venteticket',
            name='promo_client_produit',
            field=models.IntegerField(),
        ),
    ]