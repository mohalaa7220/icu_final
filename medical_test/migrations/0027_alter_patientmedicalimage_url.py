# Generated by Django 4.2 on 2023-06-29 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_test', '0026_alter_patientraysimage_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientmedicalimage',
            name='url',
            field=models.URLField(blank=True, max_length=200000),
        ),
    ]
