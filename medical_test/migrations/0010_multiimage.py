# Generated by Django 4.2 on 2023-06-20 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_test', '0009_delete_addmultiimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultiImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
    ]