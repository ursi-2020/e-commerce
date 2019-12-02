# Generated by Django 2.2.7 on 2019-12-01 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0009_produit_id_catalogue'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientPromotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IdClient', models.CharField(max_length=200)),
                ('date', models.CharField(max_length=200)),
                ('reduction', models.PositiveIntegerField()),
            ],
        ),
    ]
