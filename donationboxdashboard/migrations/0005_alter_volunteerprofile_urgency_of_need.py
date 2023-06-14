# Generated by Django 4.2.1 on 2023-06-10 17:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationboxdashboard', '0004_alter_donation_donationpic_alter_donor_userpic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteerprofile',
            name='urgency_of_need',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)]),
        ),
    ]