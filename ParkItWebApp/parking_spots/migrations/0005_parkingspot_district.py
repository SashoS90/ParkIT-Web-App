# Generated by Django 4.2.3 on 2023-07-29 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_spots', '0004_remove_parkingspot_spaces_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingspot',
            name='district',
            field=models.CharField(default='unset', max_length=40),
        ),
    ]