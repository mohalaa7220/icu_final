# Generated by Django 4.2 on 2023-04-28 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0002_alter_medicines_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
