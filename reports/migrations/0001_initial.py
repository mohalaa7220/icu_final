# Generated by Django 4.2 on 2023-04-16 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NurseReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nurses_reports', to='users.nurse')),
                ('doctor', models.ManyToManyField(related_name='doctors_reports', to='users.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patients_reports', to='users.patient')),
            ],
            options={
                'verbose_name': 'Nurse Report',
                'verbose_name_plural': 'Nurse Report',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='DoctorReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_reports', to='users.doctor')),
                ('nurse', models.ManyToManyField(related_name='nurse_reports', to='users.nurse')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_reports', to='users.patient')),
            ],
            options={
                'verbose_name': 'Doctor Report',
                'verbose_name_plural': 'Doctor Report',
                'ordering': ['-created'],
            },
        ),
    ]
