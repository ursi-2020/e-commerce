# Generated by Django 3.0.1 on 2020-01-17 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0012_tickets_venteticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
