# Generated by Django 4.2.3 on 2023-07-29 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_spots', '0005_parkingspot_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingspot',
            name='district',
            field=models.CharField(max_length=40),
        ),
    ]
