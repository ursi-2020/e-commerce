# Generated by Django 2.2.6 on 2019-10-23 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_auto_20191022_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='id_catalogue',
            field=models.PositiveIntegerField(default=3),
            preserve_default=False,
        ),
    ]
