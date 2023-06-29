# Generated by Django 4.2 on 2023-06-29 18:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_test', '0020_alter_patientraysimage_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientmedicalimage',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='patientraysimage',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None),
        ),
    ]