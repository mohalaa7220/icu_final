# Generated by Django 4.2 on 2023-04-20 12:13

from django.db import migrations, models
import django.db.models.deletion
import medical_test.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('medical_test', '0002_alter_medicaltest_options_patientmedicalimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientmedicalimage',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_medical_image', to='users.patient'),
        ),
        migrations.CreateModel(
            name='PatientRaysImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=medical_test.models.upload_to)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_rays_image', to='users.patient')),
            ],
        ),
    ]
