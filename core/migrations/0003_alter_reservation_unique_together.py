# Generated by Django 5.0.6 on 2024-06-18 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_car_alter_reservation_car'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('car', 'from_date', 'to_date')},
        ),
    ]
