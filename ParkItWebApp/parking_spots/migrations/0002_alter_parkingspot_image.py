# Generated by Django 4.2.3 on 2023-07-15 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_spots', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingspot',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]