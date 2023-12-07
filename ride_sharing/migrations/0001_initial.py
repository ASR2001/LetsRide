# Generated by Django 5.0 on 2023-12-06 09:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Requester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('asset_capacity', models.IntegerField()),
                ('travel_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AssestTransportationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('asset_type', models.CharField(choices=[('LAPTOP', 'Vehicle'), ('TRAVEL_BAG', 'Travel Bag'), ('PACKAGE', 'Package')], max_length=100)),
                ('number_of_assets', models.IntegerField()),
                ('sensitivity', models.CharField(choices=[('HIGHLY_SENSITIVE', 'Highly Sensitive'), ('SENSITIVE', 'Sensitive'), ('NORMAL', 'Normal')], max_length=100)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted')], max_length=100)),
                ('request_date', models.DateField()),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='ride_sharing.requester')),
                ('matched_riders', models.ManyToManyField(related_name='matched_requests', to='ride_sharing.rider')),
            ],
        ),
    ]
