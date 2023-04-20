# Generated by Django 4.2 on 2023-04-20 12:11

from django.db import migrations, models
import django.db.models.deletion
import medical_test.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('medical_test', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='medicaltest',
            options={'verbose_name': 'Medical Test', 'verbose_name_plural': 'Medical Test'},
        ),
        migrations.CreateModel(
            name='PatientMedicalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=medical_test.models.upload_to)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_image', to='users.patient')),
            ],
        ),
    ]