# Generated by Django 5.0 on 2023-12-06 13:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride_sharing', '0003_alter_assettransportationrequest_requester_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rider',
            name='travel_medium',
            field=models.CharField(choices=[('Car', 'Car'), ('Bus', 'Bus'), ('Train', 'Train')], default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assettransportationrequest',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted')], default='PENDING', max_length=100),
        ),
    ]
