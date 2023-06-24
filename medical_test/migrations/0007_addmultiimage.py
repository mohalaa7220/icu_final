# Generated by Django 4.2 on 2023-06-20 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_is_headnursing'),
        ('medical_test', '0006_patientmedicalimage_image_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddMultiImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.JSONField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
            ],
        ),
    ]