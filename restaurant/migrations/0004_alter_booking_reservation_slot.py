# Generated by Django 5.0.1 on 2024-04-21 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_remove_booking_comment_remove_booking_guest_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='reservation_slot',
            field=models.CharField(max_length=100),
        ),
    ]