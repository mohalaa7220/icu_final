# Generated by Django 4.2 on 2023-06-20 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_test', '0013_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='images',
        ),
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
