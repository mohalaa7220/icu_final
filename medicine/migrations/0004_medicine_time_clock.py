# Generated by Django 4.2 on 2023-04-30 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0003_medicine_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='time_clock',
            field=models.TimeField(null=True),
        ),
    ]