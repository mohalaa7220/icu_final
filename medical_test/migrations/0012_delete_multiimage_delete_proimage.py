# Generated by Django 4.2 on 2023-06-20 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical_test', '0011_proimage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MultiImage',
        ),
        migrations.DeleteModel(
            name='ProImage',
        ),
    ]
